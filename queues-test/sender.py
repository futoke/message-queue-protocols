import time

import zmq
import nanomsg
import pika # RabbitMQ
import stomp # ActiveMQ

PORT = 5555
MSG_SIZE = 1000
MSG = b'0' * MSG_SIZE
MSG_COUNT = 1000000

def zmq_pubsub_send():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://0.0.0.0:{}'.format(PORT))

    while True:
        socket.send(MSG)


def zmq_bus_send():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind('tcp://127.0.0.1:{}'.format(PORT))

    while True:
        socket.send(MSG)


def nanomsg_pubsub_send():
    with nanomsg.Socket(nanomsg.PUB) as socket:
        socket.bind('tcp://0.0.0.0:{}'.format(PORT))
        while True:
            socket.send(MSG)


def nanomsg_bus_send():
    with nanomsg.Socket(nanomsg.BUS) as socket:
        socket.bind('tcp://0.0.0.0:{}'.format(PORT))
        while True:
            socket.send(MSG)


def rabbitmq_pubsub_send():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='test', type='fanout')

    for msg in range(MSG_COUNT):
        channel.basic_publish(exchange='test', routing_key='', body=MSG)

    connection.close()


def activemq_pubsub_send():
    class MyListener(stomp.ConnectionListener):
        def __init__(self):
            super().__init__()
            self.cnt = 0
            self.start = time.time()

        def on_error(self, headers, message):
            print('received an error {}'.format(message))

        def on_message(self, headers, message):
            self.cnt += 1
            if self.cnt == MSG_COUNT - 1:
                end = time.time()
                print(MSG_COUNT / (end - self.start))


    conn = stomp.Connection()
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect('admin', 'password', wait=True)

    conn.subscribe(destination='/topic/test', id=1, ack='auto')

    for i in range(MSG_COUNT):
        conn.send(body=MSG, destination='/topic/test')

    time.sleep(2)
    conn.disconnect()



if __name__ == '__main__':
    # zmq_pubsub_send()
    # zmq_bus_send()
    nanomsg_pubsub_send()
    # nanomsg_bus_send()
    # rabbitmq_pubsub_send()
    # activemq_pubsub_send()

