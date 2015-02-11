FROM docker_pythonbase
MAINTAINER Gigaspaces, cosmo-admin@gigaspaces.com

COPY NOTICE.txt /root/NOTICE.txt

# Used by 'cfy status' impl to determine if running in container.
ENV VERSION=master \
    REST_VERSION=master \
    COMMON_VERSION=CFY-1838-separate-services-container \
    SCRIPT_VERSION=master \
    DOCKER_ENV=True \
    SERVICE_DIR=/opt/mgmtworker
ENV VIRTUALENV_DIR=${SERVICE_DIR}/env \
    CELERY_LOG_DIR=${SERVICE_DIR}/logs \
    CELERY_WORK_DIR=${SERVICE_DIR}/work \
    RIEMANN_CONFIGS_DIR=${SERVICE_DIR}/../riemann \
    BROKER_URL=amqp://guest:guest@rabbitmq:5672/ \
    MANAGEMENT_USER=root \
    MANAGER_REST_PORT=8100 \
    MANAGER_FILE_SERVER_URL=http://fileserver:53229 \
    MANAGER_FILE_SERVER_BLUEPRINTS_ROOT_URL=http://fileserver:53229/blueprints \
    CELERY_TASK_SERIALIZER=json \
    CELERY_RESULT_SERIALIZER=json \
    CELERY_RESULT_BACKEND=amqp \
    C_FORCE_ROOT=true

RUN apt-get update && \
    apt-get install -y python-dev curl unzip g++ && \
    mkdir -p ${CELERY_LOG_DIR} && \
    virtualenv ${VIRTUALENV_DIR} && \
    ${VIRTUALENV_DIR}/bin/pip install celery==3.1.17 && \
    ${VIRTUALENV_DIR}/bin/pip install https://github.com/cloudify-cosmo/cloudify-rest-client/archive/${REST_VERSION}.zip && \
    ${VIRTUALENV_DIR}/bin/pip install https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/${COMMON_VERSION}.zip && \
    ${VIRTUALENV_DIR}/bin/pip install https://github.com/cloudify-cosmo/cloudify-script-plugin/archive/${SCRIPT_VERSION}.zip && \
    cd /tmp && \
    curl -O -L https://github.com/cloudify-cosmo/cloudify-manager/archive/${VERSION}.zip && \
    unzip ${VERSION}.zip && \
    ${VIRTUALENV_DIR}/bin/pip install cloudify-manager-${VERSION}/plugins/plugin-installer && \
    ${VIRTUALENV_DIR}/bin/pip install cloudify-manager-${VERSION}/plugins/agent-installer && \
    ${VIRTUALENV_DIR}/bin/pip install cloudify-manager-${VERSION}/plugins/riemann-controller && \
    ${VIRTUALENV_DIR}/bin/pip install cloudify-manager-${VERSION}/workflows && \
    apt-get purge -y python-dev curl unzip g++ && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /root/.cache /var/lib/apt/lists/* /tmp/* /var/log/apt/*

CMD ${VIRTUALENV_DIR}/bin/celery worker \
    --include=cloudify_system_workflows.deployment_environment,plugin_installer.tasks,worker_installer.tasks,riemann_controller.tasks,cloudify.plugins.workflows \
    --broker=${BROKER_URL} \
    --hostname celery.cloudify.management \
    --events \
    --app=cloudify \
    --loglevel=debug \
    --queues=cloudify.management \
    --logfile=${CELERY_LOG_DIR}/cloudify.management_worker.log \
    --pidfile=${CELERY_LOG_DIR}/cloudify.management_worker.pid \
    --autoscale=5,2