from abc import ABC, abstractmethod

class NotificationService(ABC):
    """Classe base para serviços de notificação."""

    def send_notification(self, recipient, message):
        """Template method para enviar notificações."""
        self.log("Iniciando envio de notificação...")
        if not self.validate_recipient(recipient):
            raise ValueError("Destinatário inválido.")
        
        self.prepare_notification(recipient, message)
        self.dispatch_notification(recipient, message)
        self.log(f"Notificação enviada com sucesso para {recipient}.")

    @abstractmethod
    def validate_recipient(self, recipient):
        """Valida o destinatário."""
        pass

    @abstractmethod
    def prepare_notification(self, recipient, message):
        """Prepara a notificação antes do envio."""
        pass

    @abstractmethod
    def dispatch_notification(self, recipient, message):
        """Envia a notificação para o destinatário."""
        pass

    def log(self, message):
        """Loga informações sobre o processo."""
        print(f"[LOG]: {message}")



import smtplib
from email.mime.text import MIMEText

class EmailNotification(NotificationService):
    def validate_recipient(self, recipient):
        """Valida se o destinatário é um e-mail válido."""
        return "@" in recipient and "." in recipient

    def prepare_notification(self, recipient, message):
        """Prepara o e-mail."""
        self.log(f"Preparando e-mail para {recipient}.")

    def dispatch_notification(self, recipient, message):
        """Envia o e-mail via MailHog."""
        smtp_server = "localhost"
        smtp_port = 1025  # Porta padrão do MailHog

        msg = MIMEText(message)
        msg["Subject"] = "Notificação de Teste"
        msg["From"] = "no-reply@example.com"
        msg["To"] = recipient

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.sendmail(msg["From"], recipient, msg.as_string())
            self.log(f"E-mail enviado para {recipient}.")
        except Exception as e:
            self.log(f"Erro ao enviar e-mail: {e}")
            raise


import requests

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
if __name__ == "__main__":
    # Instanciar os serviços
    email_service = EmailNotification()
    push_service = PushNotification()

    # Enviar notificação por e-mail
    try:
        email_service.send_notification("user@example.com", "Este é um e-mail de teste via MailHog.")
    except Exception as e:
        print(f"Erro: {e}")

    # Enviar notificação por push
    try:
        push_service.send_notification("http://example.com/device", "Esta é uma notificação push via Mercure.")
    except Exception as e:
        print(f"Erro: {e}")
