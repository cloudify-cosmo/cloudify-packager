# description "Celery Management Worker"
#
# The following are to be injected by docker installation process:
#   CELERY_HOME_DIR - virtualenv path
#   CELERY_LOG_DIR - a predefined log dir
#
if [ -z "MANAGEMENT_IP" ]; then
	echo 'MANAGEMENT_IP must be provided.'
	exit 1
fi
export $MANAGEMENT_IP
export BROKER_URL="amqp://guest:guest@$MANAGEMENT_IP:5672//"
# todo(adaml): this var should be injected since it propogates to the agent nodes.
export MANAGEMENT_USER="root"
export MANAGER_REST_PORT="8100"
# todo(adaml): this var should be injected since it propogates to the agent nodes.
export VIRTUALENV="$CELERY_HOME_DIR/env"
export IS_MANAGEMENT_NODE="True"
export AGENT_IP="cloudify.management"
export MANAGER_FILE_SERVER_URL="http://$MANAGEMENT_IP:53229"
export MANAGER_FILE_SERVER_BLUEPRINTS_ROOT_URL="http://$MANAGEMENT_IP:53229/blueprints"
export CELERY_TASK_SERIALIZER="json"
export CELERY_RESULT_SERIALIZER="json"
export CELERY_RESULT_BACKEND="amqp://"
export RIEMANN_CONFIGS_DIR="$CELERY_HOME_DIR/../riemann"

exec $CELERY_HOME_DIR/env/bin/python -m celery.bin.celeryd \
    --include=cloudify_system_workflows.deployment_environment,plugin_installer.tasks,worker_installer.tasks,riemann_controller.tasks,cloudify.plugins.workflows \
    --broker=amqp:// \
    -n celery.cloudify.management \
    --events \
    --app=cloudify \
    --loglevel=debug \
    -Q cloudify.management \
    --logfile=$CELERY_LOG_DIR/cloudify.management_worker.log \
    --pidfile=$CELERY_LOG_DIR/cloudify.management_worker.pid \
    --autoscale=5,2
