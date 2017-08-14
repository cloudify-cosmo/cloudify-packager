#!/bin/bash

function print_params() {

    echo "## print common parameters"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Build on OSX"
    else
        declare -A params=( ["VERSION"]=$VERSION ["PRERELEASE"]=$PRERELEASE ["BUILD"]=$BUILD \
                        ["CORE_TAG_NAME"]=$CORE_TAG_NAME )
        for param in "${!params[@]}"
        do
            echo "$param - ${params["$param"]}"
        done
    fi
}

function install_common_prereqs () {

    echo "## install common prerequisites"
    if  which yum >> /dev/null; then
        sudo yum -y install openssl
        SUDO="sudo"
    elif which apt-get >> /dev/null; then
        sudo apt-get update &&
        sudo apt-get -y install openssl
        SUDO="sudo"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing on OSX"
        #SUDO="sudo"
    else
        echo 'probably windows machine'
    fi
    curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
    $SUDO python get-pip.py
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
    #date=$(date +"%a, %d %b %Y %T %z")
    #acl="x-amz-acl:public-read"
    #content_type='application/x-compressed-exe'
    #string="PUT\n\n$content_type\n$date\n$acl\n/$AWS_S3_BUCKET/$AWS_S3_PATH/$file"
    #signature=$(echo -en "${string}" | openssl sha1 -hmac "${AWS_ACCESS_KEY}" -binary | base64)

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
    
#     curl -v -X PUT -T "$file" \
#       -H "Host: $AWS_S3_BUCKET.s3.amazonaws.com" \
#       -H "Date: $date" \
#       -H "Content-Type: $content_type" \
#       -H "$acl" \
#       -H "Authorization: AWS ${AWS_ACCESS_KEY_ID}:$signature" \
#       "https://$AWS_S3_BUCKET.s3.amazonaws.com/$AWS_S3_PATH/$file" &&
#     echo "## successfully uploaded $file"
}

print_params
