# description     "amqp-influxdb consumer instance"
#
# The following are to be injected by docker installation process:
#   MANAGER_VIRTUALENV_DIR - path to the manager virtualenv
#
$MANAGER_VIRTUALENV_DIR/bin/python $MANAGER_VIRTUALENV_DIR/bin/cloudify-amqp-influxdb \
    --amqp-exchange cloudify-monitoring \
    --amqp-routing-key '*' \
     --influx-database cloudifyvars