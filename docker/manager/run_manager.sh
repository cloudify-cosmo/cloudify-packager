# description "manager gunicorn"
#
# The following are to be injected by docker installation process:
#   MANAGER_REST_CONFIG_PATH - path to the manager virtualenv
#   MANAGER_VIRTUALENV_DIR - path to the manager virtualenv
#   SERVER_FILES_DIR - path to server.py main entry dir
#
export MANAGER_REST_CONFIG_PATH=$MANAGER_REST_CONFIG_PATH

# calculate number of workers according to number of cores. (1-1 ratio)
WORKERS=$(($(nproc)*2+1))

# run the server service using predefined virtual env
source $MANAGER_VIRTUALENV_DIR/bin/activate
pushd $SERVER_FILES_DIR
gunicorn  -w ${WORKERS} -b 0.0.0.0:8100 --timeout 300 server:app
