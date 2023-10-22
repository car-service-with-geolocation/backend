import smtplib
import os

from email.mime.text import MIMEText


def send_email(data, send_to):
    host = os.getenv('EMAIL_HOST')
    sender = os.getenv('EMAIL_HOST_USER')
    password = os.getenv('EMAIL_HOST_PASSWORD')
    port = int(os.getenv('EMAIL_PORT'))

    server = smtplib.SMTP(host, port)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(data)
        msg["Subject"] = "Привет! Это Car Service"
        server.sendmail(sender, send_to, msg.as_string())
        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main():
    message = input().strip()
    send_to = input().strip()
    send_email(send_to, message)


if __name__ == 'main':
    main()
