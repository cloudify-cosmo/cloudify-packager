SET REST_CLIENT_SHA=
SET COMMON_PLUGIN_SHA=
SET MANAGER_SHA=
SET SCRIPTS_PLUGIN_SHA=
SET DIAMOND_PLUGIN_SHA=

cd c:\\
virtualenv CloudifyAgent
md C:\\CloudifyAgent\\nssm\
copy C:\\Tools\\nssm.exe C:\\CloudifyAgent\\nssm\\nssm.exe
cd CloudifyAgent
call Scripts\\activate.bat
pip install celery==3.0.24
pip install pyzmq==14.3.1
git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
cd C:\\CloudifyAgent\\cloudify-rest-client
if not (%REST_CLIENT_SHA%)==() git reset --hard %REST_CLIENT_SHA%
pip install .
cd C:\\CloudifyAgent
git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
cd C:\\CloudifyAgent\\cloudify-plugins-common
if not (%COMMON_PLUGIN_SHA%)==() git reset --hard %COMMON_PLUGIN_SHA%
pip install .
cd C:\\CloudifyAgent
git clone https://github.com/cloudify-cosmo/cloudify-script-plugin.git
cd C:\\CloudifyAgent\\cloudify-script-plugin
if not (%SCRIPTS_PLUGIN_SHA%)==() git reset --hard %SCRIPT_PLUGIN_SHA%
pip install .
cd C:\\CloudifyAgent
git clone https://github.com/cloudify-cosmo/cloudify-diamond-plugin.git
cd C:\\CloudifyAgent\\cloudify-diamond-plugin
if not (%DIAMOND_PLUGIN_SHA%)==() git reset --hard %DIAMOND_PLUGIN_SHA%
pip install .
cd C:\\CloudifyAgent
git clone https://github.com/cloudify-cosmo/cloudify-manager.git
cd C:\\CloudifyAgent\\cloudify-manager
if not (%MANAGER_SHA%)==() git reset --hard %MANAGER_SHA%
cd plugins\\windows-plugin-installer
pip install .
cd c:\\
rmdir /s /q C:\\CloudifyAgent\\cloudify-rest-client
rmdir /s /q C:\\CloudifyAgent\\cloudify-plugins-common
rmdir /s /q C:\\CloudifyAgent\\cloudify-manager
rmdir /s /q C:\\CloudifyAgent\\cloudify-script-plugin
rmdir /s /q C:\\CloudifyAgent\\cloudify-diamond-plugin
7z a -r -sfx -x!.* cloudify-windows-agent.exe c:\\CloudifyAgent\\*
