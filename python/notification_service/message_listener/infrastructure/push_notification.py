import requests,os,datetime,jwt

from notification_service.message_listener.interfaces.notification_service import NotificationService

class PushNotification(NotificationService):

    def __init__(self, notification_configuration):
        super().__init__(notification_configuration)
        # self.recipient = notification_configuration['recipient']
        # self.to = notification_configuration['to']
        # self.message = notification_configuration['message']
        # self.subject = notification_configuration['subject']

    def validate_recipient(self):
        """Valida o identificador do dispositivo (ex.: token)."""
        return isinstance(self.notification_configuration['recipient'], str) and len(self.notification_configuration['recipient']) > 10

    def prepare_notification(self):
        """Prepara a notificação push."""
        self.log(f"Preparando push notification para o dispositivo {self.notification_configuration['recipient']}.")

    def dispatch_notification(self):
        """Envia a notificação via Mercure."""
        hub_url = os.environ['HUB_URL']
        jwt_token = self.generate_token(os.environ['MERCURE_PUBLISHER_JWT_KEY'])

        headers = {"Authorization": f"Bearer {jwt_token}","Content-Type": "application/x-www-form-urlencoded",}
        payload = {"topic": self.notification_configuration['recipient'], "data": self.notification_configuration['body']}

        try:
            response = requests.post(hub_url, headers=headers, data=payload)
            if response.status_code == 200:
                self.log(f"Push notification enviada para {self.notification_configuration['recipient']}.")
            else:
                self.log(f"Erro ao enviar push notification: {response.status_code}, {response.text}")
                raise Exception("Falha no envio de push notification")
        except Exception as e:
            self.log(f"Erro ao enviar push notification: {e}")
            raise

    def generate_token(self,key, claim_type, topics=["*"]):
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