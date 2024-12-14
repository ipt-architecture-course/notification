import pika
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do RabbitMQ
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
rabbitmq_password = os.getenv('RABBITMQ_PASS', 'guest')
exchange_name = 'notification'

# Conectar ao RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
channel = connection.channel()

# Declarar o exchange
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

# Mensagem a ser enviada
message = json.dumps({
    'recipient':"novousuario@teste.com.br",
    'body':"""
        <html>
            <body>
                <h1>Bem-vindo ao MailHog!</h1>
                <p>Este é um exemplo de e-mail enviado no formato <b>HTML</b>.</p>
                <p><a href="https://example.com">Clique aqui</a> para saber mais.</p>
            </body>
        </html>
        """,
    'subject':'Validação de e-amil'
})
channel.basic_publish(exchange=exchange_name, routing_key='notification.email', body=message)
print(f" [x] Enviada mensagem '{message}' para o binding key notification.email")

# Notificação de Status via Email
message = json.dumps({
    'recipient':"novousuario@teste.com.br",
    'body':"""
        <html>
            <body>
                <h1>Notificação de Status Via Email</h1>
                <p>Este é um exemplo de e-mail enviado no formato <b>HTML</b>.</p>
                <p><a href="https://example.com">Clique aqui</a> para saber mais.</p>
            </body>
        </html>
        """,
    'subject':'Notificação de Status',
    'type':'email'
})
channel.basic_publish(exchange=exchange_name, routing_key='notification.status', body=message)
print(f" [x] Enviada mensagem '{message}' para o binding key notification.status")

# Notificação de Status via Push Notification
message = json.dumps({
    'recipient':"http://example.com/my-topic",
    'body':'Atualização de Perfil',
    'subject':'Notificação de Status',
    'type':'push'
})
channel.basic_publish(exchange=exchange_name, routing_key='notification.status', body=message)
print(f" [x] Enviada mensagem '{message}' para o binding key notification.status")

message = json.dumps({
    'recipient':"http://example.com/my-topic",
    'body':'Atualização de Fotos',
    'subject':'Notificação de Status',
    'type':'push'
})
channel.basic_publish(exchange=exchange_name, routing_key='notification.status', body=message)
print(f" [x] Enviada mensagem '{message}' para o binding key notification.status")


# Fechar a conexão
connection.close()
