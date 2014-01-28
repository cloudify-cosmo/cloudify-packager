#!/usr/bin/env python
import logging
import logging.config

import config
import pika
import sys

try:
    logging.config.dictConfig(config.PACKAGER_LOGGER)
    lgr = logging.getLogger('packager')
except ValueError:
    sys.exit('could not initiate logger. try sudo...')


def build_event_body(**kwargs):
    """
    receives an iterable and returns a dict
    """

    body = {}
    for field, value in kwargs.items():
        body.update({field: value})

    return str(body).replace("'", '"')


def send_event(**kwargs):
    """
    connects to an AMQP broker and registers an event
    """

    body = build_event_body(**kwargs)

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(config.RABBITMQ_HOST))
    except:
        lgr.warning('rabbitmq broker unreachable, event: %s will not be registered' % body)
        return

    channel = connection.channel()
    channel.queue_declare(queue=config.RABBITMQ_QUEUE, durable=True)
    channel.basic_publish(exchange=config.RABBITMQ_EXCHANGE,
                          routing_key=config.RABBITMQ_ROUTING_KEY,
                          body=body,
                          properties=pika.BasicProperties(delivery_mode=2))
    connection.close()


# su -s /bin/sh -c 'exec "$0" "$@"' root -- /usr/bin/java -jar /opt/logstash/logstash.jar agent -f /etc/logstash.conf
