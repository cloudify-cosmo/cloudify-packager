# This script configures and starts a PyPi mirror and http-server for cloudify offline
# Note that you should edit HOME_FOLDER and FILES_DIR variables before running this script

HOME_FOLDER="/home/vagrant"

# Expected to contain all the needed files - nginx.conf, bandersnatch.conf etc
FILES_DIR="/vagrant"

echo "Using $HOME_FOLDER as a home folder"
echo "Using $FILES_DIR as a files folder"
echo ' INSTALLING '
echo '------------'
cd "$HOME_FOLDER"
sudo apt-get update -y
echo "### Installing python-pip python-dev build-essential nginx"
sudo apt-get install python-pip python-dev build-essential nginx -y
sudo pip install --upgrade pip
sudo pip install virtualenv
sudo pip install --upgrade virtualenv
virtualenv env
source "$HOME_FOLDER/env/bin/activate"
echo "### Installing bandersnatch"
pip install -r https://bitbucket.org/pypa/bandersnatch/raw/stable/requirements.txt
echo "### Confuring nginx"
sudo mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.original # backup the original
sudo cp "$FILES_DIR/nginx.conf" /etc/nginx/nginx.conf
sudo cp "$FILES_DIR/bandersnatch.conf" /etc/nginx/sites-available/bandersnatch.conf
sudo ln -s /etc/nginx/sites-available/bandersnatch.conf /etc/nginx/sites-enabled/bandersnatch.conf
sudo mkdir /srv/cloudify
echo "### Starting nginx"
sudo nginx

echo "Creating configuration file for bandersnatch"
sudo bandersnatch mirror

echo "Using nohup to download PyPi mirror"
nohup sudo bandersnatch mirror &
PID=$!
echo "nohup pid is $PID"
echo "execute ps -m $PID to check if the download has finished"