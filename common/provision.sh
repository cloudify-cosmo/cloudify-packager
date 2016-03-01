
function print_params() {

    echo "## print common parameters"

    declare -A params=( ["VERSION"]=$VERSION ["PRERELEASE"]=$PRERELEASE ["BUILD"]=$BUILD \
                        ["CORE_TAG_NAME"]=$CORE_TAG_NAME ["PLUGINS_TAG_NAME"]=$PLUGINS_TAG_NAME )
    for param in "${!params[@]}"
    do
            echo "$param - ${params["$param"]}"
    done
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
    else
        echo 'probably windows machine'
    fi
}

function create_md5() {

    local file_ext=$1
    echo "## create md5"
    md5sum=$(md5sum -t *.$file_ext) &&
    echo $md5sum | $SUDO tee ${md5sum##* }.md5
}

function upload_to_s3() {

    local file_ext=$1
    file=$(basename $(find . -type f -name "*.$file_ext"))
    date=$(date +"%a, %d %b %Y %T %z")
    acl="x-amz-acl:public-read"
    content_type='application/x-compressed-exe'
    string="PUT\n\n$content_type\n$date\n$acl\n/$AWS_S3_BUCKET/$AWS_S3_PATH/$file"
    signature=$(echo -en "${string}" | openssl sha1 -hmac "${AWS_ACCESS_KEY}" -binary | base64)

    echo "## uploading https://$AWS_S3_BUCKET.s3.amazonaws.com/$AWS_S3_PATH/$file"

    curl -v -X PUT -T "$file" \
      -H "Host: $AWS_S3_BUCKET.s3.amazonaws.com" \
      -H "Date: $date" \
      -H "Content-Type: $content_type" \
      -H "$acl" \
      -H "Authorization: AWS ${AWS_ACCESS_KEY_ID}:$signature" \
      "https://$AWS_S3_BUCKET.s3.amazonaws.com/$AWS_S3_PATH/$file"
}


export VERSION="3.4.0"
export PRERELEASE="m3"
export BUILD="392"
export CORE_TAG_NAME="3.4m3"
export PLUGINS_TAG_NAME="1.3.1"
export AWS_S3_BUCKET="gigaspaces-repository-eu"
export AWS_S3_PATH="org/cloudify3/${VERSION}/${PRERELEASE}"


print_params
install_common_prereqs
