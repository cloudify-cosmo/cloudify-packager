
function print_params() {

    ctx logger info "Printing common parameters..."

    declare -A params=( ["VERSION"]=$VERSION ["PRERELEASE"]=$PRERELEASE ["BUILD"]=$BUILD \
                        ["CORE_TAG_NAME"]=$CORE_TAG_NAME ["PLUGINS_TAG_NAME"]=$PLUGINS_TAG_NAME )
    for param in "${!params[@]}"
    do
            ctx logger info "$param - ${params["$param"]}"
    done
}

function install_common_prereqs () {

    ctx logger info "Installing common prerequisites..."
    if  which yum >> /dev/null; then
        sudo yum -y install openssl
        SUDO="sudo"
    elif which apt-get >> /dev/null; then
        sudo apt-get update &&
        sudo apt-get -y install openssl
        SUDO="sudo"
    else
        ctx logger info 'Probably a Windows machine, skipping...'
    fi
}

function create_md5() {

    local file_ext=$1
    ctx logger info "Creating md5 checksum file for package..."
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

    ctx logger info "Uploading https://$AWS_S3_BUCKET.s3.amazonaws.com/${AWS_S3_PATH}/${file}..."

    curl -v -X PUT -T "$file" \
      -H "Host: $AWS_S3_BUCKET.s3.amazonaws.com" \
      -H "Date: $date" \
      -H "Content-Type: $content_type" \
      -H "$acl" \
      -H "Authorization: AWS ${AWS_ACCESS_KEY_ID}:$signature" \
      "https://$AWS_S3_BUCKET.s3.amazonaws.com/$AWS_S3_PATH/$file"
}


export VERSION="$(ctx node properties version)"
export PRERELEASE="$(ctx node properties prerelease)"
export BUILD="$(ctx node properties build)"
export CORE_TAG_NAME="$(ctx node properties core_tag_name)"
export PLUGINS_TAG_NAME="$(ctx node properties plugins_tag_name)"
export AWS_S3_BUCKET="$(ctx node properties aws_s3_bucket)"
export AWS_S3_PATH="$(ctx node properties aws_s3_path)"


print_params
install_common_prereqs
