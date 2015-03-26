SET CORE_TAG_NAME=
SET PLUGINS_TAG_NAME=


cd c:\\
virtualenv cfy
cd cfy
git clone git@github.com:GET-CLOUDIFY.PY-SCRIPT.git
REM download PyCrypto here somehow
call Scripts\\activate.bat
pip install wheel==0.24.0
pip wheel virtualenv==12.0.7
pip wheel git+https://github.com/cloudify-cosmo/cloudify-rest-client@%CORE_TAG_NAME% --find-links=wheelhouse
pip wheel git+https://github.com/cloudify-cosmo/cloudify-dsl-parser@%CORE_TAG_NAME% --find-links=wheelhouse
pip wheel git+https://github.com/cloudify-cosmo/cloudify-plugins-common@%CORE_TAG_NAME% --find-links=wheelhouse
pip wheel git+https://github.com/cloudify-cosmo/cloudify-script-plugin@%PLUGINS_TAG_NAME% --find-links=wheelhouse
REM wheel vSphere and SoftLayer plugins
pip wheel git+https://github.com/cloudify-cosmo/cloudify-cli@%CORE_TAG_NAME% --find-links=wheelhouse
7z a -r -sfx -x!.* Cloudify.exe c:\\cfy\\*