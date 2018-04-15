#!/bin/bash

function print_params() {

    echo "## print common parameters"

    arr[0]="VERSION=$VERSION"
    arr[1]="PRERELEASE=$PRERELEASE"
    arr[2]="CORE_BRANCH=$CORE_BRANCH"
    arr[2]="CORE_TAG_NAME=$CORE_TAG_NAME"
    echo ${arr[@]}
}

function install_common_prereqs () {

    echo "## install common prerequisites"
    if  which yum >> /dev/null; then
        sudo yum -y install openssl curl
        SUDO="sudo"
        # Setting this for Centos only, as it seems to break otherwise on 6.5
        CURL_OPTIONS="-1"
    elif which apt-get >> /dev/null; then
        sudo apt-get update &&
        sudo apt-get -y install openssl libssl-dev
        SUDO="sudo"
        if [ "`lsb_release -r -s`" == "16.04" ];then
            sudo apt-get -y install python
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing on OSX"
        SUDO="sudo"
    else
        echo 'Probably windows machine'
    fi
    
    curl $CURL_OPTIONS "https://bootstrap.pypa.io/2.6/get-pip.py" -o "get-pip.py" &&
    $SUDO python get-pip.py pip==9.0.1 &&
    $SUDO pip install wheel==0.29.0 &&
    $SUDO pip install setuptools==36.8.0 &&
    $SUDO pip install awscli &&
    echo "## end of installing common prerequisites"
    
}

function create_md5() {

    local file_ext=$1
    echo "## create md5"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        md5cmd="md5 -r"
    else
        md5cmd="md5sum -t"
    fi
    md5sum=$($md5cmd *.$file_ext) &&
    echo $md5sum | $SUDO tee ${md5sum##* }.md5
}

function upload_to_s3() {

    local file_ext=$1
    file=$(basename $(find . -type f -name "*.$file_ext"))
    
    echo "## uploading https://$AWS_S3_BUCKET.s3.amazonaws.com/$AWS_S3_PATH/$file"
    export AWS_SECRET_ACCESS_KEY=${AWS_ACCESS_KEY} &&
    export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} &&
    awscli="aws"
    if [[ "$OSTYPE" == "cygwin" ]]; then
        awscli="python `cygpath -w $(which aws)`"
    fi
    echo "$awscli s3 cp --acl public-read $file s3://$AWS_S3_BUCKET/$AWS_S3_PATH/"
    $awscli s3 cp --acl public-read $file s3://$AWS_S3_BUCKET/$AWS_S3_PATH/ &&
    echo "## successfully uploaded $file"
  
}

print_params
