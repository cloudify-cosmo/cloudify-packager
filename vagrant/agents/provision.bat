SET CORE_TAG_NAME="master"
SET PLUGINS_TAG_NAME="master"

cd c:\\
virtualenv CloudifyAgent
md C:\\CloudifyAgent\\nssm\
copy C:\\Tools\\nssm.exe C:\\CloudifyAgent\\nssm\\nssm.exe
cd CloudifyAgent
call Scripts\\activate.bat
pip install celery==3.1.17
pip install pyzmq==14.3.1
git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
cd C:\\CloudifyAgent\\cloudify-rest-client
  git checkout -b tmp_branch %CORE_TAG_NAME%
  git log -1
  pip install .
cd C:\\CloudifyAgent
git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
cd C:\\CloudifyAgent\\cloudify-plugins-common
  git checkout -b tmp_branch %CORE_TAG_NAME%
  git log -1
  pip install .
cd C:\\CloudifyAgent
git clone https://github.com/cloudify-cosmo/cloudify-script-plugin.git
cd C:\\CloudifyAgent\\cloudify-script-plugin
  git checkout -b tmp_branch %PLUGINS_TAG_NAME%
  git log -1
  pip install .
cd C:\\CloudifyAgent
git clone https://github.com/cloudify-cosmo/cloudify-diamond-plugin.git
cd C:\\CloudifyAgent\\cloudify-diamond-plugin
  git checkout -b tmp_branch %PLUGINS_TAG_NAME%
  git log -1 
  pip install .
cd C:\\CloudifyAgent
git clone https://github.com/cloudify-cosmo/cloudify-manager.git
cd C:\\CloudifyAgent\\cloudify-manager
  git checkout -b tmp_branch %CORE_TAG_NAME%
  git log -1
cd plugins\\windows-plugin-installer
pip install .
cd c:\\
rmdir /s /q C:\\CloudifyAgent\\cloudify-rest-client
rmdir /s /q C:\\CloudifyAgent\\cloudify-plugins-common
rmdir /s /q C:\\CloudifyAgent\\cloudify-manager
rmdir /s /q C:\\CloudifyAgent\\cloudify-script-plugin
rmdir /s /q C:\\CloudifyAgent\\cloudify-diamond-plugin
7z a -r -sfx -x!.* cloudify-windows-agent.exe c:\\CloudifyAgent\\*
