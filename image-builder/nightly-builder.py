from __future__ import print_function
import os
import re
import string
import random
from time import sleep, strftime
from string import Template
from tempfile import gettempdir
from StringIO import StringIO
from subprocess import Popen, PIPE

import boto.ec2
from boto.ec2 import blockdevicemapping as bdm
from fabric.api import env, run, sudo, execute, put

from settings import settings

RESOURCES = []


def main():
    print('Starting nightly build: {}'.format(strftime("%Y-%m-%d %H:%M:%S")))
    print('Opening connection..')
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_ACCESS_KEY')
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

    kp_name = random_generator()
    kp = conn.create_key_pair(kp_name)
    kp.save(gettempdir())
    print('Keypair created: {}'.format(kp_name))

    sg_name = random_generator()
    sg = conn.create_security_group(sg_name, 'vagrant nightly')
    sg.authorize(ip_protocol='tcp',
                 from_port=22,
                 to_port=22,
                 cidr_ip='0.0.0.0/0')
    print('Security Group created: {}'.format(sg_name))

    reserv = conn.run_instances(image_id=settings['factory_ami'],
                                key_name=kp_name,
                                instance_type=settings['instance_type'],
                                security_groups=[sg],
                                block_device_map=mapping,
                                instance_profile_name=settings['aws_iam_group'])

    factory_instance = reserv.instances[0]
    RESOURCES.append(factory_instance)
    RESOURCES.append(kp)
    RESOURCES.append(sg)

    env.key_filename = os.path.join(gettempdir(), '{}.pem'.format(kp_name))
    env.timeout = 10
    env.connection_attempts = 12

    while factory_instance.state != 'running':
        sleep(5)
        factory_instance.update()
        print('machine state: {}'.format(factory_instance.state))

    print('Executing script..')
    execute(do_work, host='{}@{}'.format(settings['username'],
                                         factory_instance.ip_address))


def random_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def run_packer():
    packer_cmd = 'packer build ' \
                 '-machine-readable ' \
                 '-only=nightly_virtualbox_build ' \
                 '-var-file={} ' \
                 'packerfile.json'.format(settings['packer_var_file'])
    p = Popen(packer_cmd.split(), stdout=PIPE, stderr=PIPE)

    packer_output = ''
    while True:
        line = p.stdout.readline()
        if line == '':
            break
        else:
            print(line, end="")
            if re.match('^.+artifact.+id', line):
                packer_output = line
    return packer_output.split(':')[-1].rstrip()


def do_work():
    sudo('apt-get update')
    sudo('apt-get install -y virtualbox kpartx extlinux qemu-utils python-pip')
    sudo('pip install awscli')

    sudo('mkdir -p /mnt/image')
    sudo('mount /dev/xvdf1 /mnt/image')

    run('dd if=/dev/zero of=image.raw bs=1M count=5120')
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

    box_name = 'cloudify_{}'.format(strftime('%y%m%d-%H%M'))
    box_url = 'https://s3-{0}.amazonaws.com/{1}/{2}.box'.format(
        settings['region'], settings['aws_s3_bucket'], box_name
    )
    run('aws s3 cp '
        'cloudify.box s3://{}/{}.box'.format(settings['aws_s3_bucket'],
                                             box_name))
    with open('templates/publish_Vagrantfile.template') as f:
        template = Template(f.read())
    vfile = StringIO()
    vfile.write(template.substitute(BOX_NAME=box_name,
                                    BOX_URL=box_url))
    put(vfile, 'publish_Vagrantfile')
    run('aws s3 cp publish_Vagrantfile s3://{}/{}'.format(
        settings['aws_s3_bucket'], 'Vagrantfile'))

def cleanup():
    print('cleaning up..')
    for item in RESOURCES:
        if type(item) == boto.ec2.image.Image:
            item.deregister()
            print('{} deregistered'.format(item))
        elif type(item) == boto.ec2.instance.Instance:
            item.terminate()
            while item.state != 'terminated':
                sleep(5)
                item.update()
            print('{} terminated'.format(item))
        elif type(item) == boto.ec2.connection.EC2Connection:
            item.close()
            print('{} closed'.format(item))
        elif (type(item) == boto.ec2.securitygroup.SecurityGroup or
              type(item) == boto.ec2.keypair.KeyPair):
            item.delete()
            print('{} deleted'.format(item))
        else:
            print('{} not cleared'.format(item))

try:
    main()
finally:
    cleanup()
    print('finished build: {}'.format(strftime("%Y-%m-%d %H:%M:%S")))
