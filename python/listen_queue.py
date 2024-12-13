#!/usr/bin/env python
import pika, os, logging, json
from dotenv import load_dotenv
from notification_service.message_listener.infrastructure.email_notification import EmailNotification
from notification_service.message_listener.infrastructure.push_notification import PushNotification

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Configurações do RabbitMQ
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
rabbitmq_password = os.getenv('RABBITMQ_PASS', 'guest')

# Conexão com o RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='notification', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

ROUTING_KEYS = os.environ['ROUTING_KEYS'].split(',')

# binding_keys = sys.argv[1:]
# if not binding_keys:
#     sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
#     sys.exit(1)

# for binding_key in binding_keys:
#     channel.queue_bind(
#         exchange='notification', queue=queue_name, routing_key=binding_key
#     )

for routing_key in ROUTING_KEYS:
    channel.queue_bind(exchange='notification', queue=queue_name, routing_key=routing_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


# Callback function to handle incoming messages
def callback(ch, method, properties, body):
    routing_key = method.routing_key
    logging.info(f'Received message with routing key: {routing_key}')

    notification_configuration = json.loads(body)
    logging.info(notification_configuration)
    try:
        if routing_key == 'notification.email':
            email = EmailNotification(notification_configuration=notification_configuration)
            email.send_notification()
        elif routing_key == 'notification.status':
            if notification_configuration['type'] == 'email':
                # TODO - request profile
                email = EmailNotification(notification_configuration=notification_configuration)
                email.send_notification()
            else:
                push_notificatioon = PushNotification(notification_configuration=notification_configuration)
                push_notificatioon.send_notification()
        else:
            logging.warning(f'Unhandled routing key: {routing_key}')
    except Exception as e:
        logging.error(f'Error processing message: {e}', exc_info=True)

# Start consuming messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    logging.info('Stopping consumer')
    channel.stop_consuming()
finally:
    connection.close()