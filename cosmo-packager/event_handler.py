#!/usr/bin/env python
import logging
import logging.config

import config
# import os
# run_env = os.environ['RUN_ENV']
# config = __import__(run_env)

import pika
import sys
import os

try:
    d = os.path.dirname(config.LOGGER['handlers']['file']['filename'])
    if not os.path.exists(d):
        os.makedirs(d)
    logging.config.dictConfig(config.LOGGER)
    lgr = logging.getLogger('main')
    lgr.setLevel(logging.INFO)
except ValueError:
    sys.exit('could not initialize logger.'
             ' verify your logger config'
             ' and permissions to write to {0}'
             .format(config.LOGGER['handlers']['file']['filename']))


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
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(config.RABBITMQ_HOST))
    except:
        lgr.warning('rabbitmq broker unreachable, event: '
                    '%s will not be registered' % body)
        return

    channel = connection.channel()
    channel.queue_declare(queue=config.RABBITMQ_QUEUE, durable=True)
    channel.basic_publish(exchange=config.RABBITMQ_EXCHANGE,
                          routing_key=config.RABBITMQ_ROUTING_KEY,
                          body=body,
                          properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
