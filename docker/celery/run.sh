# description "Celery Management Worker"
# The following are to be injected by docker.
# CELERY_HOME_DIR - virtualenv path

export BROKER_URL="amqp://guest:guest@localhost:5672//"
# todo(adaml): this var should be injected since it propogates to the agent nodes.
export MANAGEMENT_USER="root"
export MANAGER_REST_PORT="8100"
# todo(adaml): this var should be injected since it propogates to the agent nodes.
export MANAGEMENT_IP="localhost"
export CELERY_WORK_DIR="$CELERY_HOME_DIR/work"
export VIRTUALENV="$CELERY_HOME_DIR/env"
export IS_MANAGEMENT_NODE="True"
export AGENT_IP="cloudify.management"
export MANAGER_FILE_SERVER_URL="http://localhost:53229"
export MANAGER_FILE_SERVER_BLUEPRINTS_ROOT_URL="http://localhost:53229/blueprints"
export CELERY_TASK_SERIALIZER="json"
export CELERY_RESULT_SERIALIZER="json"
export CELERY_RESULT_BACKEND="amqp://"
export RIEMANN_CONFIGS_DIR="$CELERY_HOME_DIR/../riemann"

mkdir $CELERY_WORK_DIR/

exec $CELERY_HOME_DIR/env/bin/python -m celery.bin.celeryd \
--include=cloudify_system_workflows.deployment_environment,plugin_installer.tasks,worker_installer.tasks,riemann_controller.tasks,cloudify.plugins.workflows \
--broker=amqp:// \
-n celery.cloudify.management \
--events \
--app=cloudify \
--loglevel=debug \
-Q cloudify.management \
--logfile=$CELERY_WORK_DIR/cloudify.management_worker.log \
--pidfile=$CELERY_WORK_DIR/cloudify.management_worker.pid \
--autoscale=5,2
