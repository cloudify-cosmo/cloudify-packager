export CORE_TAG_NAME="4.0rc1"
export PLUGINS_TAG_NAME="1.3"

pip install wheel

pip wheel --wheel-dir packaging/source/wheels --requirement "https://raw.githubusercontent.com/cloudify-cosmo/cloudify-agent/$CORE_TAG_NAME/dev-requirements.txt"
pip wheel --find-links packaging/source/wheels --wheel-dir packaging/source/wheels "https://github.com/cloudify-cosmo/cloudify-agent/archive/$CORE_TAG_NAME.zip"

export VERSION=`ls packaging/source/wheels/cloudify_agent-* | cut -d"-" -f2`

echo "VERSION=$VERSION"

iscc packaging/create_install_wizard.iss
