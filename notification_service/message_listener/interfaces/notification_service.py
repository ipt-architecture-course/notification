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