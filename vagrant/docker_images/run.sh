# install vagrant - https://www.vagrantup.com/downloads.html (1.6.2) #
#vagrant plugin install vagrant-aws (0.4.1)                         #
#vagrant plugin install unf                                         #
#####################################################################

source ../../../credentials.sh
source /etc/environment

function  exit_on_error {
      status=$?
      echo "exit code="$status    
      if [ $status != 0 ] ; then
         	echo "Failed (exit code $status)" 
		#vagrant destroy -f ubuntu            
		exit 1
      fi

}

sudo mkdir -p /cloudify_tmp
sudo chown tgrid -R /cloudify_tmp
rm -f /cloudify_tmp/cloudify-*.tar


##destroy ubuntu vm if exit
vagrant destroy -f ubuntu

vagrant up ubuntu --provider=aws
exit_on_error

##get guest ip address
ip_address=`vagrant ssh-config ubuntu | grep HostName | sed "s/HostName//g" | sed "s/ //g"`
echo "ip_address="$ip_address

##copy tar files
sudo mkdir -p /cloudify_tmp
sudo chown tgrid -R /cloudify_tmp
scp -i ~/.ssh/aws/vagrant_build.pem ubuntu@$ip_address:/tmp/*.tar /cloudify_tmp
exit_on_error

vagrant destroy -f ubuntu
