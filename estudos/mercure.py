import requests

# Configuração do Mercure
hub_url = "http://localhost:3000/.well-known/mercure"
jwt_token = "!changeThisMercureHubJWTSecretKey!"

# Dados da notificação
topic = "http://example.com/test"
data = "Esta é uma notificação de teste."

# Enviar a notificação
headers = {"Authorization": f"Bearer {jwt_token}"}
payload = {"topic": topic, "data": data}
response = requests.post(hub_url, headers=headers, data=payload)

if response.status_code == 200:
    print("Notificação enviada com sucesso!")
else:
    print(f"Erro ao enviar notificação: {response.status_code}, {response.text}")
