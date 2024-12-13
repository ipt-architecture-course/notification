import jwt
import datetime

# Chaves secretas definidas no docker-compose
PUBLISHER_KEY = "!ChangeThisPublisherKey!"
SUBSCRIBER_KEY = "!ChangeThisSubscriberKey!"

hub_url = "http://localhost:80/.well-known/mercure"

def generate_token(key, claim_type, topics=["*"]):
    """
    Gera um token JWT para publicar ou subscrever mensagens no Mercure.

    :param key: Chave secreta (PUBLISHER_KEY ou SUBSCRIBER_KEY)
    :param claim_type: Tipo de permissão ('publish' ou 'subscribe')
    :param topics: Lista de tópicos permitidos (default: ["*"])
    :return: Token JWT
    """
    payload = {
        "mercure": {claim_type: topics},
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expira em 1 hora
    }
    token = jwt.encode(payload, key, algorithm="HS256")
    return token

# Exemplo de uso:
publisher_token = generate_token(PUBLISHER_KEY, "publish")
subscriber_token = generate_token(SUBSCRIBER_KEY, "subscribe")

print("Publisher Token:", publisher_token)
print("Subscriber Token:", subscriber_token)



import requests

# def publish_message(token, topic, data, hub_url):
#     """
#     Publica uma mensagem no Mercure.

#     :param token: Token JWT para autenticação
#     :param topic: Tópico da mensagem
#     :param data: Dados da mensagem
#     :param hub_url: URL do Mercure Hub
#     """
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     payload = {
#         "topic": topic,
#         "data": data,
#     }
#     response = requests.post(hub_url, headers=headers, data=payload, verify=False)
#     return response.status_code, response.text

# # Exemplo de uso:
topic = "http://example.com/my-topic"
# data = "Hello, World!"
# status, response = publish_message(publisher_token, topic, data,hub_url)
# print(f"Status: {status}, Response: {response}")



import sseclient

def subscribe_to_topic(token, topic, hub_url):
    """
    Inscreve-se em um tópico e escuta mensagens.

    :param token: Token JWT para autenticação
    :param topic: Tópico desejado
    :param hub_url: URL do Mercure Hub
    """
    url = f"{hub_url}?topic={topic}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers, stream=True)
    client = sseclient.SSEClient(response)

    print(f"Listening to topic: {topic}")
    for event in client.events():
        print(f"Mensagem recebida: {event.data}")

# Exemplo de uso:
subscribe_to_topic(subscriber_token, topic,hub_url)
