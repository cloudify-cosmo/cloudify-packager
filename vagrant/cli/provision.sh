function install_prereqs
{
    if which apt-get; then
        # ubuntu
        sudo apt-get -y update &&
        # precise
        sudo apt-get install -y python-software-properties ||
        # trusty
        sudo apt-get install -y software-properties-common &&
        sudo add-apt-repository -y ppa:git-core/ppa &&
        sudo apt-get install -y curl python-dev git make gcc libyaml-dev zlib1g-dev g++ rpm
    elif which yum; then
        # centos/REHL
        sudo yum -y update &&
        sudo yum install -y yum-downloadonly wget mlocate yum-utils &&
        sudo yum install -y python-devel libyaml-devel ruby rubygems ruby-devel make gcc git g++ rpm-build
    else
        echo 'unsupported package manager, exiting'
        exit 1
    fi
}

function install_ruby
{
    wget https://ftp.ruby-lang.org/pub/ruby/ruby-1.9.3-rc1.tar.bz2 --no-check-certificate
    tar -xjf ruby-1.9.3-rc1.tar.bz2
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
    if which apt-get; then
        curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
    else
        curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python2.7
    fi
}

function install_module
{

    module=$1
    venv=${2:-""}
    tag=${3:-""}
    if [[ ! -z "$tag" ]]; then
        org=${4:-cloudify-cosmo}
        url=https://github.com/${org}/${module}.git
        echo cloning ${url}
        git clone ${url}
        pushd ${module}
            git checkout -b tmp_branch ${tag}
            git log -1
            sudo ${venv}/bin/pip install .
        popd
    else
        if [[ ! -z "$venv" ]]; then
            # if [[ ! -z "$tag" ]]; then
            #   pip install git+git://github.com/${org}/${module}.git@${tag}#egg=${module}
            # else
            sudo ${venv}/bin/pip install ${module}
            # fi
        else
            sudo pip install ${module}
        fi
    fi
}

function install_py27
{
    # install python and additions
    # http://bicofino.io/blog/2014/01/16/installing-python-2-dot-7-6-on-centos-6-dot-5/
    sudo yum groupinstall -y 'development tools'
    sudo yum install -y zlib-devel bzip2-devel openssl-devel xz-libs
    sudo mkdir /py27
    cd /py27
    sudo wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
    sudo xz -d Python-2.7.6.tar.xz
    sudo tar -xvf Python-2.7.6.tar
    cd Python-2.7.6
    sudo ./configure --prefix=/usr
    sudo make
    sudo make altinstall
}


CORE_TAG_NAME="master"
PLUGINS_TAG_NAME="master"

install_prereqs &&
if which apt-get; then
    install_ruby
fi
if which yum; then
    install_py27
fi
install_fpm &&
install_pip &&
install_module "https://github.com/cloudify-cosmo/packman/archive/pkm-overhaul.zip" &&
install_module "wheel==0.24.0" &&

sudo mkdir -p /cfy && cd /cfy &&

echo '# GET PROCESS'
sudo pip wheel virtualenv==12.0.7 &&
# when the cli is built for py2.6, unless argparse is put within `install_requires`, we'll have to enable this:
# if which yum; then
#   pip wheel argparse==#SOME_VERSION#
# fi

sudo pip wheel git+https://github.com/cloudify-cosmo/cloudify-rest-client@${CORE_TAG_NAME} --find-links=wheelhouse &&
sudo pip wheel git+https://github.com/cloudify-cosmo/cloudify-dsl-parser@${CORE_TAG_NAME} --find-links=wheelhouse &&
sudo pip wheel git+https://github.com/cloudify-cosmo/cloudify-plugins-common@${CORE_TAG_NAME} --find-links=wheelhouse &&
sudo pip wheel git+https://github.com/cloudify-cosmo/cloudify-script-plugin@${PLUGINS_TAG_NAME} --find-links=wheelhouse &&
sudo pip wheel git+https://github.com/cloudify-cosmo/cloudify-cli@${CORE_TAG_NAME} --find-links=wheelhouse

cd /cloudify-packager/ && sudo pkm pack -c cloudify-linux-cli -v