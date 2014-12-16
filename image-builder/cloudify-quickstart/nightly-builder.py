from __future__ import print_function
import boto.ec2
from boto.ec2 import blockdevicemapping as bdm
from os import environ
from fabric.api import env, run, sudo, execute
from settings import settings
from time import sleep


def main():
    print('Opening connection..')
    conn = get_conn()
    print('Running Packer..')
    baked_ami = run_packer()
    baked_snap = get_snapshot(conn, baked_ami)

    print('Launching worker machine..')
    mapping = bdm.BlockDeviceMapping()
    mapping['/dev/sda1'] = bdm.BlockDeviceType(size=10,
                                               volume_type='gp2',
                                               delete_on_termination=True)
    mapping['/dev/sdf'] = bdm.BlockDeviceType(snapshot_id=baked_snap,
                                              volume_type='gp2',
                                              delete_on_termination=True)

    factory_instance = launch_instance(conn,
                                       image_id=settings['factory_ami'],
                                       key_name=settings['keypair_name'],
                                       instance_type=settings['instance_type'],
                                       security_groups=['default'],
                                       block_device_map=mapping)

    env.key_filename = settings['keypair_path']
    env.timeout = 10
    env.connection_attempts = 12

    while (factory_instance.state != 'running' or
           factory_instance.ip_address is None):
        sleep(5)
        factory_instance.update()
        print('machine state: {}\n'
              'machine IP: {}'.format(factory_instance.state,
                                      factory_instance.ip_address))

    print('Executing script..')
    execute(do_work, host='{}@{}'.format(settings['username'],
                                         factory_instance.ip_address))


def get_conn():
    access_key = environ.get('aws_access_key', settings['aws_access_key'])
    secret_key = environ.get('aws_secret_key', settings['aws_secret_key'])
    conn = boto.ec2.connect_to_region(settings['region'],
                                      aws_access_key_id=access_key,
                                      aws_secret_access_key=secret_key)
    return conn


def launch_instance(conn, **kwargs):
    reserv = conn.run_instances(**kwargs)
    instance = reserv.instances[0]
    return instance


def get_snapshot(conn, ami):
    sda1 = conn.get_all_images(ami)[0].block_device_mapping['/dev/sda1']
    sda1_snap = sda1.snapshot_id
    print('snapshot id: {}'.format(sda1_snap))
    return sda1_snap


def run_packer():
    # this should probably run local()
    return 'ami-80f64ff7'


def do_work():
    sudo('apt-get update')
    sudo('apt-get install -y virtualbox kpartx extlinux qemu-utils')

    sudo('mkdir -p /mnt/image')
    sudo('mount /dev/xvdf1 /mnt/image')

    run('dd if=/dev/zero of=image.raw bs=1M count=3072')
    sudo('losetup --find --show image.raw')
    sudo('parted -s -a optimal /dev/loop0 mklabel msdos'
         ' -- mkpart primary ext4 1 -1')
    sudo('parted -s /dev/loop0 set 1 boot on')
    sudo('kpartx -av /dev/loop0')
    sudo('mkfs.ext4 /dev/mapper/loop0p1')
    sudo('mkdir -p /mnt/raw')
    sudo('mount /dev/mapper/loop0p1 /mnt/raw')

    sudo('cp -a /mnt/image/* /mnt/raw')

    sudo('extlinux --install /mnt/raw/boot')
    sudo('dd if=/usr/lib/syslinux/mbr.bin conv=notrunc bs=440 count=1 '
         'of=/dev/loop0')
    # sudo('echo "UUID=`sudo blkid -s UUID -o value /dev/mapper/loop0p1`'
    #      '   /   ext4   defaults   0   1" | sudo -s tee /mnt/raw/etc/fstab')
    sudo('echo -e "DEFAULT cloudify\n'
         'LABEL cloudify\n'
         'LINUX /vmlinuz\n'
         'APPEND root=/dev/disk/by-uuid/'
         '`sudo blkid -s UUID -o value /dev/mapper/loop0p1` ro\n'
         'INITRD  /initrd.img" | sudo -s tee /mnt/raw/boot/extlinux.conf')

    sudo('umount /mnt/raw')
    sudo('kpartx -d /dev/loop0')
    sudo('losetup --detach /dev/loop0')

    run('qemu-img convert -f raw -O vmdk image.raw image.vmdk')
    run('rm image.raw')

    run('mkdir output')
    run('VBoxManage createvm --name cloudify --ostype Ubuntu_64 --register')
    run('VBoxManage storagectl cloudify '
        '--name SATA '
        '--add sata '
        '--sataportcount 1 '
        '--hostiocache on '
        '--bootable on')
    run('VBoxManage storageattach cloudify '
        '--storagectl SATA '
        '--port 0 '
        '--type hdd '
        '--medium image.vmdk')
    run('VBoxManage modifyvm cloudify '
        '--vram 12 '
        '--ioapic on '
        '--rtcuseutc on '
        '--pae off')
    run('VBoxManage export cloudify --output output/box.ovf')

    run('echo "Vagrant::Config.run do |config|" > output/Vagrantfile')
    run('echo "  config.vm.base_mac = `VBoxManage showvminfo cloudify '
        '--machinereadable | grep  macaddress1 | cut -d"=" -f2`"'
        ' >> output/Vagrantfile')
    run('echo -e "end\n\n" >> output/Vagrantfile')
    run('echo \'include_vagrantfile = File.expand_path'
        '("../include/_Vagrantfile", __FILE__)\' >> output/Vagrantfile')
    run('echo "load include_vagrantfile if File.exist?'
        '(include_vagrantfile)" >> output/Vagrantfile')
    run('echo \'{ "provider": "virtualbox" }\' > output/metadata.json')
    run('tar -cvf cloudify.box -C output/ .')
    # upload to s3?
main()
