import requests

from notification_service.message_listener.interfaces.notification_service import NotificationService

class PushNotification(NotificationService):
    def validate_recipient(self, recipient):
        """Valida o identificador do dispositivo (ex.: token)."""
        return isinstance(recipient, str) and len(recipient) > 10

    def prepare_notification(self, recipient, message):
        """Prepara a notificação push."""
        self.log(f"Preparando push notification para o dispositivo {recipient}.")

    def dispatch_notification(self, recipient, message):
        """Envia a notificação via Mercure."""
        hub_url = "http://localhost:3000/.well-known/mercure"
        jwt_token = "!changeThisMercureHubJWTSecretKey!"  # Substituir pela chave configurada

        headers = {"Authorization": f"Bearer {jwt_token}"}
        payload = {"topic": recipient, "data": message}

        try:
            response = requests.post(hub_url, headers=headers, data=payload)
            if response.status_code == 200:
                self.log(f"Push notification enviada para {recipient}.")
            else:
                self.log(f"Erro ao enviar push notification: {response.status_code}, {response.text}")
                raise Exception("Falha no envio de push notification")
        except Exception as e:
            self.log(f"Erro ao enviar push notification: {e}")
            raise