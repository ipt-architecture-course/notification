
from notification_service.message_listener.infrastructure.push_notification import PushNotification
from notification_service.message_listener.infrastructure.email_notification import EmailNotification


if __name__ == "__main__":
    # Instanciar os serviços
    email_service = EmailNotification()
    push_service = PushNotification()

    # Enviar notificação por e-mail
    # try:
    #     email_service.send_notification("user@example.com", "Este é um e-mail de teste via MailHog.")
    # except Exception as e:
    #     print(f"Erro: {e}")

    # Enviar notificação por push
    # try:
    #     push_service.send_notification("http://example.com/device", "Esta é uma notificação push via Mercure.")
    # except Exception as e:
    #     print(f"Erro: {e}")
