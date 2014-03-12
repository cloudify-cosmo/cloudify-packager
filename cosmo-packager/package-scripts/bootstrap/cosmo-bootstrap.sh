BOOTSTRAP_DIR="/cosmo-bootstrap"

echo "bootstraping cosmo"
dpkg -i ${BOOTSTRAP_DIR}/openjdk-7jdk/*.deb
dpkg -i ${BOOTSTRAP_DIR}/logstash/*.deb
dpkg -i ${BOOTSTRAP_DIR}/elasticsearch/*.deb
dpkg -i ${BOOTSTRAP_DIR}/nginx/*.deb
dpkg -i ${BOOTSTRAP_DIR}/nodejs/*.deb
dpkg -i ${BOOTSTRAP_DIR}/riemann/*.deb
dpkg -i ${BOOTSTRAP_DIR}/rabbitmq-server/*.deb
dpkg -i ${BOOTSTRAP_DIR}/jruby/*.deb
