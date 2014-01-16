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
    sends an event to an AMQP broker
    """

    body = build_event_body(**kwargs)

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(config.RABBITMQ_HOST))
    except:
        lgr.warning('rabbitmq broker unreachable, event: %s will not be registered' % body)
        return
    channel = connection.channel()

    channel.queue_declare(queue=config.RABBITMQ_QUEUE)

    channel.basic_publish(exchange='',
                          routing_key='packager',
                          body=body)
    connection.close()
