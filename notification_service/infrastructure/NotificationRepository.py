from notification_service.domain.interfaces.irepository import INotificationRepository

class NotificationRepository(INotificationRepository):
    def __init__(self):
        super().__init__()