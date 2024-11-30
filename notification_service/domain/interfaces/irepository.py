from abc import ABC, abstractmethod

class INotificationRepository(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def send_notification(self):
        pass