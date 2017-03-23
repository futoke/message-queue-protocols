import time
import sys
import zmq
import nanomsg
import pika

PORT = 5555
MSG_COUNT = 10000


def zmq_pubsub_recv():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:{}".format(PORT))
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    start = time.time()

    for i in range(MSG_COUNT):
        socket.recv()

    end = time.time()
    print(MSG_COUNT / (end - start))


def zmq_bus_recv():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://127.0.0.1:{}".format(PORT))

    start = time.time()

    for i in range(MSG_COUNT):
        socket.recv()

    end = time.time()
    print(MSG_COUNT / (end - start))


def nanomsg_pubsub_recv():
    with nanomsg.Socket(nanomsg.SUB) as socket:
        socket.connect("tcp://futoke.ru:{}".format(PORT))
        socket.set_string_option(nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, '')

        start = time.time()

        for i in range(MSG_COUNT):
            socket.recv()

        end = time.time()
        print(MSG_COUNT / (end - start))


def nanomsg_bus_recv():
    with nanomsg.Socket(nanomsg.BUS) as socket:
        socket.connect("tcp://futoke.ru:{}".format(PORT))

        start = time.time()

        for i in range(MSG_COUNT):
            socket.recv()

        end = time.time()
        print(MSG_COUNT / (end - start))


cnt = 0

def rabbitmq_pubsub_recv():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='test', type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='test', queue=queue_name)

    start = time.time()

    def callback(ch, method, properties, body):
        global cnt
        cnt += 1
        if cnt == MSG_COUNT - 1:
            end = time.time()
            print(MSG_COUNT / (end - start))
            sys.exit(0)

    channel.basic_consume(callback, queue=queue_name, no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    # zmq_pubsub_recv()
    # zmq_bus_recv()
    # nanomsg_pubsub_recv()
    nanomsg_bus_recv()
    # rabbitmq_pubsub_recv()