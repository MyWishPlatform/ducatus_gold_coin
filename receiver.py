import pika
import os
import traceback
import threading
import json
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gold_coin.settings')
import django

django.setup()

from gold_coin.settings import NETWORK_SETTINGS
from gold_coin.transfer.api import TransferReceiver


class Receiver(threading.Thread):

    def __init__(self, queue):
        super().__init__()
        self.network = queue

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost',
            5672,
            'gold_coin',
            pika.PlainCredentials('gold_coin', 'gold_coin'),
        ))

        channel = connection.channel()

        queue_name = NETWORK_SETTINGS[self.network]['queue']

        channel.queue_declare(
            queue=queue_name,
            durable=True,
            auto_delete=False,
            exclusive=False
        )
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.callback
        )

        print(
            'RECEIVER MAIN: started on {net} with queue `{queue_name}`'
                .format(net=self.network, queue_name=queue_name), flush=True
        )

        channel.start_consuming()

    def duc_transfer(self, message):
        print('PAYMENT MESSAGE RECEIVED', flush=True)
        TransferReceiver.parse_duc_message(message)

    def erc_transfer(self, message):
        print('TRANSFER CONFIRMATION RECEIVED', flush=True)
        TransferReceiver.parse_erc_message(message)

    def callback(self, ch, method, properties, body):
        print('received', body, properties, method, flush=True)
        try:
            message = json.loads(body.decode())
            if message.get('status', '') == 'COMMITTED':
                getattr(self, properties.type, self.unknown_handler)(message)
        except Exception as e:
            print('\n'.join(traceback.format_exception(*sys.exc_info())),
                  flush=True)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def unknown_handler(self, message):
        print('unknown message', message, flush=True)


networks = NETWORK_SETTINGS.keys()

if __name__ == '__main__':
    for network in networks:
        rec = Receiver(network)
        rec.start()
