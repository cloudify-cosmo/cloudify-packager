# description "Influxdb service"
#
# The following are to be injected by docker installation process:
#   INFLUXDB_CONFIG_FILE - path to influxdb configuration file
#
/usr/bin/influxdb -config=$INFLUXDB_CONFIG_FILE