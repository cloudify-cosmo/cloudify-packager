FROM ubuntu:12.04
MAINTAINER adaml, adaml@gigaspaces.com
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - BASE
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add all init and config files
ADD conf/ /opt/tmp/conf/
ADD init/ /opt/tmp/init/
# add utility functions
ADD utils/ /opt/tmp/utils/

# allow rc policies
RUN sed -i 's/101/0/g' /usr/sbin/policy-rc.d

# update local cache
RUN apt-get update
# install 3rd party components
#RUN apt-get install -y \
#    python-dev \
#    make \
#    curl \
#    openjdk-7-jdk \
#    python-software-properties \
#    g++ \
#    logrotate \
#    vim \
#    mlocate

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - RABBITMQ, DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies.
RUN apt-get install -y $(echo ['curl', 'logrotate', 'erlang-nox'] | tr -d "',[]")
# download rabbit package
RUN curl http://www.rabbitmq.com/releases/rabbitmq-server/v3.2.4/rabbitmq-server_3.2.4-1_all.deb --create-dirs -o /opt/tmp/rabbitmq/rabbitmq-server.deb

ENV RABBITMQ_SERVICE_NAME rabbitmq-server
ENV RABBITMQ_INIT_FILE /opt/tmp/init/$RABBITMQ_SERVICE_NAME.conf

# place init script in local init dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $RABBITMQ_INIT_FILE /etc/init/ && \
    check_file "/etc/init/$RABBITMQ_SERVICE_NAME.conf"'

# install and run rabbitmq-server
RUN dpkg -i /opt/tmp/rabbitmq/rabbitmq-server.deb && \
    rabbitmq-plugins enable rabbitmq_management && \
    rabbitmq-plugins enable rabbitmq_tracing && \
    invoke-rc.d $RABBITMQ_SERVICE_NAME stop && \
    invoke-rc.d $RABBITMQ_SERVICE_NAME start && \
    rabbitmqctl trace_on
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - RIEMANN, DependsOn: langohr
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies.
RUN apt-get install -y $(echo ['curl', 'openjdk-7-jdk'] | tr -d "',[]")
# download and set permissions on langohr jar.
RUN curl https://s3-eu-west-1.amazonaws.com/gigaspaces-repository-eu/langohr/2.11.0/langohr.jar --create-dirs -o /usr/lib/riemann/langohr.jar && \
    chmod 644 /usr/lib/riemann/langohr.jar
# download riemann deb
RUN curl http://aphyr.com/riemann/riemann_0.2.6_all.deb --create-dirs -o /opt/tmp/riemann/riemann.deb

##### ENV #####
ENV RIEMANN_SERVICE_NAME riemann
# riemann init file
ENV RIEMANN_INIT_FILE /opt/tmp/init/$RIEMANN_SERVICE_NAME.conf
ENV RIEMANN_SERVICE_DIR /opt/$RIEMANN_SERVICE_NAME/
##### ENV #####

# inject required env vars to init script
RUN sed -i '1s|^|RIEMANN_JAR_PATH='$RIEMANN_SERVICE_DIR$(basename /usr/lib/riemann/langohr.jar)' \n|' $RIEMANN_INIT_FILE
# todo(adaml): inject init script the proper config path according to riemann-controller plugin path

# place jar in service dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
# place init script in local init dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $RIEMANN_INIT_FILE /etc/init/ && \
    check_file "/etc/init/$RIEMANN_SERVICE_NAME.conf"'

    mv /usr/lib/riemann/langohr.jar $RIEMANN_SERVICE_DIR && \
    check_file "$RIEMANN_SERVICE_DIR$(basename /usr/lib/riemann/langohr.jar)"'
# install riemann
RUN dpkg -i /opt/tmp/riemann/riemann.deb

# todo(adaml): start riemann

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - NODEJS DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies.
#RUN apt-get install -y $(echo [] | tr -d "',[]")
# download and install
RUN add-apt-repository -y ppa:chris-lea/node.js && \
	apt-get update && \
    apt-get install -y nodejs
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - LOGSTASH DependsOn: ~
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies.
RUN apt-get install -y $(echo ['curl', 'openjdk-7-jdk'] | tr -d "',[]")
# download jar file
RUN curl https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar --create-dirs -o /opt/tmp/logstash/logstash.jar

##### ENV #####
ENV LOGSTASH_SERVICE_NAME logstash
ENV LOGSTASH_SERVICE_DIR /opt/$LOGSTASH_SERVICE_NAME/
# logstash init file
ENV LOGSTASH_INIT_FILE /opt/tmp/init/$LOGSTASH_SERVICE_NAME.conf
# logstash conf file
ENV LOGSTASH_CONF_FILE /opt/tmp/conf/$LOGSTASH_SERVICE_NAME.conf
##### ENV #####

# inject required env vars to init script
RUN sed -i '1s|^|LOGSTASH_JAR_PATH='$LOGSTASH_SERVICE_DIR$(basename /opt/tmp/logstash/logstash.jar)' \n|' $LOGSTASH_INIT_FILE
RUN sed -i '1s|^|LOGSTASH_CONF_PATH='/etc/$LOGSTASH_SERVICE_NAME.conf' \n|' $LOGSTASH_INIT_FILE

# create service dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mkdir -p $LOGSTASH_SERVICE_DIR && \
    check_dir "$LOGSTASH_SERVICE_DIR"'

# place jar in service dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv /opt/tmp/logstash/logstash.jar $LOGSTASH_SERVICE_DIR && \
    check_file "$LOGSTASH_SERVICE_DIR$(basename /opt/tmp/logstash/logstash.jar)"'
# place init script in local init dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $LOGSTASH_INIT_FILE /etc/init/ && \
    check_file "/etc/init/$LOGSTASH_SERVICE_NAME.conf"'
# place conf script in conf dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $LOGSTASH_CONF_FILE /etc/ && \
    check_file "/etc/$LOGSTASH_SERVICE_NAME.conf"'

# start logstash
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    start $LOGSTASH_SERVICE_NAME && \
    check_upstart $LOGSTASH_SERVICE_NAME'

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - ELASTICSEARCH
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies
RUN apt-get install -y $(echo ['curl', 'openjdk-7-jdk'] | tr -d "',[]")
# download binaries
RUN curl https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz --create-dirs -o /opt/tmp/elasticsearch/elasticsearch.tar.gz

##### ENV #####
ENV ELASTICSEARCH_SERVICE_NAME elasticsearch
ENV ELASTICSEARCH_SERVICE_DIR /opt/$ELASTICSEARCH_SERVICE_NAME/
##### ENV #####

# create service dir
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mkdir -p $ELASTICSEARCH_SERVICE_DIR && \
    check_dir "$ELASTICSEARCH_SERVICE_DIR"'

# extract binaries to service dir
RUN tar -C $ELASTICSEARCH_SERVICE_DIR -xvf /opt/tmp/elasticsearch/elasticsearch.tar.gz --strip-components=1

# start elasticsearch as daemon for configuration purpeses.
# config includes setting elasticsearch indexes.
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    ${ELASTICSEARCH_SERVICE_DIR}bin/elasticsearch -d && \
    wait_for_port 9200' && \
    curl --retry 5 --retry-delay 3 -XDELETE http://localhost:9200/cloudify_storage && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage -d '{"settings": {"analysis": {"analyzer": {"default": {"tokenizer": "whitespace"}}}}}' && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/blueprint/_mapping -d '{"blueprint": {"properties": {"plan": {"enabled": false}}}}' && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/deployment/_mapping -d '{"deployment": {"properties": {"plan": {"enabled": false}, "workflows": {"enabled": false}}}}' && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/node/_mapping -d '{ "node": { "_id": { "path": "id" }, "properties": { "types": { "type": "string", "index_name": "type" }, "properties": { "enabled": false } } } }' && \
    curl --retry 5 --retry-delay 3 -XPUT http://localhost:9200/cloudify_storage/node_instance/_mapping -d '{ "node_instance": { "_id": { "path": "id" }, "properties": { "runtime_properties": { "enabled": false } } } }' && \
    curl --retry 5 --retry-delay 3 -XGET http://localhost:9200/cloudify_storage/_mapping?pretty=1

# start elasticsearch as non-daemon
CMD ["ES_JAVA_OPTS=-Xmx1024m -Xms1024m; /opt/elasticsearch/bin/elasticsearch"]

# expose elasticsearch port
EXPOSE 9200

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - INFLUXDB
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# install dependencies
RUN apt-get install -y $(echo ['curl'] | tr -d "',[]")
# download binaries
RUN curl http://s3.amazonaws.com/influxdb/influxdb_0.8.0_amd64.deb --create-dirs -o /opt/tmp/influxdb.deb
##### ENV #####
ENV INFLUXDB_SERVICE_NAME influxdb
# default influxdb config path
ENV INFLUXDB_CONFIG_FILE /opt/influxdb/shared/config.toml
##### ENV #####

# todo(adaml): allow ability to configure ssl and default ports via config file. this should be done using a script.
# RUN sed -i -r -e 's/^# ssl-/ssl-/g' -e 's/^port *= * 8086/# port = 8086/' $INFLUXDB_CONFIG_FILE

# install influxdb
RUN dpkg -i /opt/tmp/influxdb.deb

# start influxdb as daemon and create cloudify db
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    /usr/bin/influxdb-daemon -config=$INFLUXDB_CONFIG_FILE && \
    wait_for_port 8086' && \
    curl -s "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}"

# run the service as non-daemon
CMD ["/usr/bin/influxdb -config=/opt/influxdb/shared/config.toml"]

# expose api port
EXPOSE 8086
# expose admin port
EXPOSE 8083
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - NGINX
# ------------------------------------------------------------------------------------------------------------------------------------------ #
# add nginx repositories to sources.list file and update repo
RUN echo ['deb http://nginx.org/packages/mainline/ubuntu/ precise nginx', 'deb-src http://nginx.org/packages/mainline/ubuntu/ precise nginx'] | tr -d "'["| tr ',]' '\n' >> /etc/apt/sources.list && \
    apt-get update
# install dependencies
RUN apt-get install -y $(echo ['curl'] | tr -d "',[]")

# set nginx service name
ENV NGINX_SERVICE_NAME nginx
# nginx conf file
ENV NGINX_CONF_FILE /opt/tmp/conf/default.conf

# download and add signing key
RUN curl http://nginx.org/keys/nginx_signing.key --create-dirs -o /opt/tmp/nginx/nginx_signing.key && \
    apt-key add /opt/tmp/nginx/nginx_signing.key

# install nginx
RUN apt-get install -y --force-yes $NGINX_SERVICE_NAME

# place config file in config path
RUN /bin/bash -c 'source /opt/tmp/utils/bootstrap_utils.sh && \
    mv $NGINX_CONF_FILE /etc/nginx/conf.d && \
    check_file "/etc/nginx/conf.d/default.conf"'

# turn-off daemon execution
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Define default command.
CMD ["/usr/sbin/nginx"]

# Expose ports.
EXPOSE 80

# ------------------------------------------------------------------------------------------------------------------------------------------ #
# CONTAINER - CELERY
# ------------------------------------------------------------------------------------------------------------------------------------------ #
RUN curl https://codeload.github.com/cloudify-cosmo/cloudify-manager/tar.gz/master --create-dirs -o /opt/tmp/celery/manager.tar.gz && \
    mkdir -p /opt/celery/cloudify.management__worker/env && \
    tar -C /opt/celery/cloudify.management__worker/env -xzvf /opt/tmp/celery/manager.tar.gz && \
    virtualenv /opt/celery/cloudify.management__worker/env && \
    /opt/celery/cloudify.management__worker/env/bin/pip install https://github.com/cloudify-cosmo/cloudify-rest-client/archive/master.tar.gz && \
    /opt/celery/cloudify.management__worker/env/bin/pip install https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/master.tar.gz && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/plugins/agent-installer/ && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/plugins/plugin-installer/ && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/plugins/riemann-controller/ && \
    /opt/celery/cloudify.management__worker/env/bin/pip install /opt/celery/cloudify.management__worker/env/cloudify-manager-master/workflows/