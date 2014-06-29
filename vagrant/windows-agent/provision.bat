SET REST_CLIENT_SHA=
SET PLUGIN_COMMON_SHA=
SET OS_PROVIDER_SHA=


cd c:\\ 
virtualenv Cloudify-Agent 
md C:\\Cloudify-Agent\\nssm\ 
copy C:\\Tools\\nssm.exe C:\\Cloudify-Agent\\nssm\\nssm.exe 
cd Cloudify-Agent 
call Scripts\\activate.bat 
git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git 
cd C:\\Cloudify-Agent\\cloudify-rest-client 
if not (%REST_CLIENT_SHA%)==() git reset --hard %REST_CLIENT_SHA% 
pip install . -r dev-requirements.txt
cd C:\\Cloudify-Agent
git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
cd C:\\Cloudify-Agent\\cloudify-plugins-common
if not (%PLUGIN_COMMON_SHA%)==() git reset --hard %PLUGIN_COMMON_SHA%
pip install . 
cd C:\\Cloudify-Agent
git clone https://github.com/cloudify-cosmo/cloudify-manager.git
cd C:\\Cloudify-Agent\\cloudify-manager
if not (%MANAGER_SHA%)==() git reset --hard %MANAGER_SHA% 
cd plugins\\plugin-installer 
pip install . 
cd c:\\ 
rmdir /s /q C:\\Cloudify-Agent\\cloudify-rest-client
rmdir /s /q C:\\Cloudify-Agent\\cloudify-plugins-common
rmdir /s /q C:\\Cloudify-Agent\\cloudify-manager 
7z a -r -sfx -x!.* Cloudify.exe c:\\Cloudify-Agent\\*
