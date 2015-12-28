class RHELBase(object):

    @property
    def local_env_blueprint_file_name(self):
        return 'start-ec2-worker-vm.yaml'

    @property
    def manager_blueprint_file_name(self):
        return 'aws-ec2-manager-blueprint.yaml'

    @property
    def app_blueprint_file(self):
        return 'ec2-blueprint.yaml'

    @property
    def client_cfy_work_dir(self):
        return '/opt/cfy'

    @property
    def region(self):
        return self.env.ec2_region_name

    @property
    def deployment_inputs(self):
        return {
            'image_id': self.image_name,
            'instance_type': self.env.medium_instance_type,
            'agent_user': self.env.rhel_7_image_user
        }

    @property
    def bootstrap_inputs(self):
        return {
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.env.ec2_region_name,
            'manager_keypair_name': '{0}-manager-keypair'.format(self.prefix),
            'agent_keypair_name': '{0}-agent-keypair'.format(self.prefix),
            'ssh_user': 'centos',
            'agents_user': 'centos',
            'image_id': self.env.centos_7_image_id,
            'instance_type': self.env.medium_instance_type,
            'ssh_key_filename': '~/.ssh/{0}-cloudify-manager-kp.pem'.format(
                self.prefix),
        }

    @property
    def local_env_inputs(self):
        return {
            'prefix': self.prefix,
            'image_id': self.image_name,
            'instance_type': self.env.medium_instance_type,
            'aws_access_key_id': self.env.aws_access_key_id,
            'aws_secret_access_key': self.env.aws_secret_access_key,
            'ec2_region_name': self.region,
            'key_pair_path': '{0}/{1}-keypair.pem'.format(self.workdir,
                                                          self.prefix)
        }

    def add_dns_nameservers_to_manager_blueprint(self, *args, **kwargs):
        pass


class RHEL7Base(RHELBase):
    @property
    def client_user(self):
        return self.env.rhel_7_image_user

    @property
    def image_name(self):
        return self.env.rhel_7_image_id

    @property
    def package_parameter_name(self):
        return 'RHEL_CLI_PACKAGE_URL'


class RHEL65Base(RHELBase):

    @property
    def client_user(self):
        return self.env.rhel_7_image_user

    @property
    def image_name(self):
        return self.env.rhel_65_image_id

    @property
    def package_parameter_name(self):
        return 'CENTOS_6_5_CLI_PACKAGE_URL'
