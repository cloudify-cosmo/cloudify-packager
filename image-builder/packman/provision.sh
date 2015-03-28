function install_prereqs
{
    # some of these are not related to the image specifically but rather to processes that will be executed later
    # such as git, python-dev and make
    if which apt-get; then
        # ubuntu
        sudo apt-get -y update &&
        # the commented below might not be required. If the latest version of git is required, we'll have to enable them
        # precise - python-software-properties
        # trusty - software-properties-common
        # sudo apt-get install -y software-properties-common
        # sudo apt-get install -y python-software-properties
        # sudo add-apt-repository -y ppa:git-core/ppa &&
        sudo apt-get install -y curl python-dev git make gcc libyaml-dev zlib1g-dev g++
    elif which yum; then
        # centos/REHL
        sudo yum -y update &&
        sudo yum install -y yum-downloadonly wget mlocate yum-utils &&
        sudo yum install -y python-devel libyaml-devel ruby rubygems ruby-devel make gcc git g++
        # this is required to build pyzmq under centos/RHEL
        sudo yum install -y zeromq-devel -c http://download.opensuse.org/repositories/home:/fengshuo:/zeromq/CentOS_CentOS-6/home:fengshuo:zeromq.repo
    else
        echo 'unsupported package manager, exiting'
        exit 1
    fi
}

function install_ruby
{
    wget https://ftp.ruby-lang.org/pub/ruby/ruby-1.9.3-rc1.tar.gz --no-check-certificate
    # alt since ruby-lang's ftp blows
    # wget http://mirrors.ibiblio.org/ruby/1.9/ruby-1.9.3-rc1.tar.gz --no-check-certificate
    tar -xzvf ruby-1.9.3-rc1.tar.gz
    cd ruby-1.9.3-rc1
    ./configure --disable-install-doc
    make
    sudo make install
    cd ~
}

function install_fpm
{
    sudo gem install fpm --no-ri --no-rdoc
    # if we want to downlod gems as a part of the packman run, this should be enabled
    # echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> ~/.gemrc
}

function install_pip
{
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
}

install_prereqs &&
if ! which ruby; then
    install_ruby
fi
install_fpm &&
install_pip &&
sudo pip install "packman==0.5.0" &&
sudo pip install "virtualenv==12.0.7" &&
sudo pip install "boto==2.36.0"
