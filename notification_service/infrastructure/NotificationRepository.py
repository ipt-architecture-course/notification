from notification_service.domain.interfaces.irepository import INotificationRepository

class NotificationRepository(INotificationRepository):
    def __init__(self):
        super().__init__()

    def send_notification(self):
        return super().send_notification()