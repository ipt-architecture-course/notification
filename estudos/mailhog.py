import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração do servidor SMTP de teste
smtp_server = "localhost"
smtp_port = 1025  # Porta usada pelo MailHog

# Informações do e-mail
from_email = "teste@example.com"
to_email = "destinatario@example.com"
subject = "Teste de envio de e-mail"
body = "Este é um e-mail enviado para fins de teste com MailHog."

# Criar o e-mail
msg = MIMEMultipart()
msg["From"] = from_email
msg["To"] = to_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# Enviar o e-mail
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(from_email, to_email, msg.as_string())
    print("E-mail enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar o e-mail: {e}")
