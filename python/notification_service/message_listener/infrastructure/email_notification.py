import smtplib,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from notification_service.message_listener.interfaces.notification_service import NotificationService

class EmailNotification(NotificationService):

    def __init__(self, notification_configuration):
        super().__init__(notification_configuration)
        # self.recipient = notification_configuration['recipient']
        # self.to = notification_configuration['to']
        # self.message = notification_configuration['message']
        # self.subject = notification_configuration['subject']

    def validate_recipient(self):
        """Valida se o destinatário é um e-mail válido."""
        return "@" in self.notification_configuration['recipient'] and "." in self.notification_configuration['recipient']

    def prepare_notification(self):
        """Prepara o e-mail."""
        self.log(f"Preparando e-mail para {self.notification_configuration['recipient']}.")

    def dispatch_notification(self):
        """Envia o e-mail via MailHog."""
        smtp_server = os.environ['SMTP_SERVER']
        smtp_port = os.environ['SMTP_PORT']

        msg = MIMEMultipart("alternative")
        msg["Subject"] = self.notification_configuration['subject']
        msg["From"] = os.environ["SENDER_MAIL"]
        msg["To"] = self.notification_configuration['recipient']
        msg.attach(MIMEText(self.notification_configuration['body'], "html"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.sendmail(msg["From"], self.notification_configuration['recipient'], msg.as_string())
            self.log(f"E-mail enviado para {self.notification_configuration['recipient']}.")
        except Exception as e:
            self.log(f"Erro ao enviar e-mail: {e}")
            raise