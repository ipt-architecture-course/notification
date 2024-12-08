# import pika
# import sys
# import os
# import time
# import email_service
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# RABBITMQ_URL = os.environ.get("RABBITMQ_URL")
    

# def main():
#     # rabbitmq connection
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_URL))
#     channel = connection.channel()

#     def callback(ch, method, properties, body):
#         try:
#             err = email_service.notification(body)
#             if err:
#                 ch.basic_nack(delivery_tag=method.delivery_tag)
#             else:
#                 ch.basic_ack(delivery_tag=method.delivery_tag)
#         except Exception as e:
#             print(f"Error processing message: {e}")
#             ch.basic_nack(delivery_tag=method.delivery_tag)

#     channel.basic_consume(queue="email_notification", on_message_callback=callback)

#     print("Waiting for messages. To exit press CTRL+C")

#     channel.start_consuming()


# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("Interrupted")
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)

# import pika

# def queue1_callback(ch, method, properties, body):
#     print(" [x] Received queue 1: %r" % body)

# def queue2_callback(ch, method, properties, body):
#     print(" [x] Received queue 2: %r" % body)

# def on_open(connection):
#     connection.channel(on_open_callback = on_channel_open)


# def on_channel_open(channel):
#     channel.basic_consume('email_notification', queue1_callback, auto_ack = True)
#     channel.basic_consume('status_notification', queue2_callback, auto_ack = True)
#     channel.basic_qos(prefetch_count=1)

# # credentials = pika.PlainCredentials('u', 'p')
# parameters = pika.ConnectionParameters('localhost') #, 5672, '/', credentials)
# connection = pika.SelectConnection(parameters = parameters, on_open_callback = on_open)

# try:
#     connection.ioloop.start()
# except KeyboardInterrupt:
#     connection.close()
#     connection.ioloop.start()


#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='notification', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()