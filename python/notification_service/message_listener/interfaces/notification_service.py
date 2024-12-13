from abc import ABC, abstractmethod

class NotificationService(ABC):
    """Classe base para serviços de notificação."""

    def __init__(self, notification_configuration:dict[str:str]):
        super().__init__()
        self.notification_configuration = notification_configuration

    def send_notification(self):
        """Template method para enviar notificações."""
        self.log("Iniciando envio de notificação...")
        if not self.validate_recipient():
            raise ValueError("Destinatário inválido.")
        
        self.prepare_notification()
        self.dispatch_notification()
        self.log("Notificação enviada com sucesso.")

    @abstractmethod
    def validate_recipient(self):
        """Valida o destinatário."""
        pass

    @abstractmethod
    def prepare_notification(self):
        """Prepara a notificação antes do envio."""
        pass

    @abstractmethod
    def dispatch_notification(self):
        """Envia a notificação para o destinatário."""
        pass

    def log(self, message):
        """Loga informações sobre o processo."""
        print(f"[LOG]: {message}")