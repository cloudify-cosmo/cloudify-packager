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
        sudo yum -y install openssl ca-certificates curl
        SUDO="sudo"
    elif which apt-get >> /dev/null; then
        sudo apt-get update &&
        sudo apt-get -y install openssl
        SUDO="sudo"
        if [ "`lsb_release -r -s`" == "16.04" ];then
            sudo apt-get -y install python
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing on OSX"
    else
        echo 'Probably windows machine'
    fi
    
    curl -1 "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
    $SUDO python get-pip.py
    $SUDO pip install wheel==0.29.0
    $SUDO pip install awscli
    
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
