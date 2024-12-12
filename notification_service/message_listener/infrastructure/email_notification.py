import smtplib
from email.mime.text import MIMEText

from notification_service.message_listener.interfaces.notification_service import NotificationService

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