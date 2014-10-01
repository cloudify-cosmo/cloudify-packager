# description "manager gunicorn"
# environment vars be injected by docker:
#   MANAGER_REST_CONFIG_PATH - path to the manager virtualenv
#   MANAGER_VIRTUALENV_DIR - path to the manager virtualenv

export MANAGER_REST_CONFIG_PATH=$MANAGER_REST_CONFIG_PATH
WORKERS=$(($(nproc)*2+1))
$MANAGER_VIRTUALENV_DIR/bin/gunicorn  -w ${WORKERS} -b 0.0.0.0:8100 --timeout 300 server:app
