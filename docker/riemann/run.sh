# The following will be injected to script by docker
# RIEMANN_JAR_PATH - Actual jar path
# MANAGER_CONFIG_PATH - Actual config path

export EXTRA_CLASSPATH=$RIEMANN_JAR_PATH
if [ -f ${MANAGER_CONFIG_PATH} ]; then
    CONFIG_PATH=${MANAGER_CONFIG_PATH}
fi
/usr/bin/riemann -a ${CONFIG_PATH}