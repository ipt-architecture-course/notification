import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do MailHog
SMTP_SERVER = "localhost"
SMTP_PORT = 1025

# Configurações do e-mail
sender_email = "remetente@example.com"
recipient_email = "destinatario@example.com"
subject = "Teste de E-mail para o MailHog"
body = """
Olá,

Este é um e-mail de teste enviado para o MailHog.

Atenciosamente,
Equipe de Testes
"""

# Criar a mensagem
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = subject

# Adicionar o corpo do e-mail
message.attach(MIMEText(body, "plain"))

try:
    # Conexão com o servidor SMTP do MailHog
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.sendmail(sender_email, recipient_email, message.as_string())
    print(f"E-mail enviado com sucesso para {recipient_email}")
except Exception as e:
    print(f"Erro ao enviar o e-mail: {e}")
