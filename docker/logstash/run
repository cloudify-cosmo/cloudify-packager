# description "Logstash -service"
#
# The following are to be injected by docker installation process:
#   LOGSTASH_JAR_PATH - path to logstash service jar
#   LOGSTASH_CONF_PATH - path to logstash configuration file
#
exec /usr/bin/java \
    -jar $LOGSTASH_JAR_PATH agent \
    -f $LOGSTASH_CONF_PATH