from __future__ import print_function
import csv
from os import environ
from time import sleep, strftime

import boto.ec2
from boto.ec2 import blockdevicemapping as bdm
from fabric.api import env, run, sudo, execute, local

from settings import settings

RESOURCES = []


def main():
    print('Opening connection..')
    access_key = environ.get('aws_access_key', settings['aws_access_key'])
    secret_key = environ.get('aws_secret_key', settings['aws_secret_key'])
    conn = boto.ec2.connect_to_region(settings['region'],
                                      aws_access_key_id=access_key,
                                      aws_secret_access_key=secret_key)
    RESOURCES.append(conn)

    print('Running Packer..')
    baked_ami_id = run_packer()
    baked_ami = conn.get_image(baked_ami_id)
    RESOURCES.append(baked_ami)

    baked_snap = baked_ami.block_device_mapping['/dev/sda1'].snapshot_id

    print('Launching worker machine..')
    mapping = bdm.BlockDeviceMapping()
    mapping['/dev/sda1'] = bdm.BlockDeviceType(size=10,
                                               volume_type='gp2',
                                               delete_on_termination=True)
    mapping['/dev/sdf'] = bdm.BlockDeviceType(snapshot_id=baked_snap,
                                              volume_type='gp2',
                                              delete_on_termination=True)

    reserv = conn.run_instances(image_id=settings['factory_ami'],
                                key_name=settings['keypair_name'],
                                instance_type=settings['instance_type'],
                                security_groups=['default'],
                                block_device_map=mapping,
                                instance_profile_name=settings['aws_iam_group'])

    factory_instance = reserv.instances[0]
    RESOURCES.append(factory_instance)

    env.key_filename = settings['keypair_path']
    env.timeout = 10
    env.connection_attempts = 12

    while factory_instance.state != 'running':
        sleep(5)
        factory_instance.update()
        print('machine state: {}'.format(factory_instance.state))

    print('Executing script..')
    execute(do_work, host='{}@{}'.format(settings['username'],
                                         factory_instance.ip_address))


def run_packer():
    packer_cmd = '/usr/local/bin/packer build ' \
                 '-machine-readable ' \
                 '-only=nightly_virtualbox_build ' \
                 '-var-file={} ' \
                 'packerfile.json'.format(settings['packer_var_file'])
    print('starting packer..')
    output = local(packer_cmd, capture=True)
    print(output.stdout)
    return get_ami_from_output(output.stdout)


def get_ami_from_output(output):
    csv_reader = csv.reader(output.split('\n'))
    for row in csv_reader:
        if row[2] == 'artifact' and row[4] == 'id':
            return row[-1].split(':')[-1]


def do_work():
    sudo('apt-get update')
    sudo('apt-get install -y virtualbox kpartx extlinux qemu-utils python-pip')
    sudo('pip install awscli')

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
        '--memory 2048 '
        '--cpus 2 '
        '--vram 12 '
        '--ioapic on '
        '--rtcuseutc on '
        '--pae off '
        '--boot1 disk '
        '--boot2 none '
        '--boot3 none '
        '--boot4 none ')
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

    box_name = 'cloudify_{}.box'.format(strftime('%y%m%d-%H%M'))
    run('aws s3 cp cloudify.box s3://{}/{}'.format(settings['aws_s3_bucket'],
                                                   box_name))


def cleanup():
    print('cleaning up..')
    for item in RESOURCES:
        if type(item) == boto.ec2.image.Image:
            item.deregister()
            print('ami {} deregistered'.format(item))
        elif type(item) == boto.ec2.instance.Instance:
            item.terminate()
            print('instance {} terminated'.format(item))
        elif type(item) == boto.ec2.connection.EC2Connection:
            item.close()
            print('connection {} closed'.format(item))
        else:
            print('{} not cleared'.format(item))

try:
    main()
finally:
    cleanup()
