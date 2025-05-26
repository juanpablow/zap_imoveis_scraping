import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv


def send_email_with_csv(path_file, subject="Imóveis comerciais atualizados"):
    load_dotenv()
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")
    senha = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_from
    msg["To"] = email_to
    msg.set_content("Segue em anexo a lista de imóveis comerciais atualizada.")

    with open(path_file, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(path_file)

    msg.add_attachment(
        file_data, maintype="application", subtype="octet-stream", filename=file_name
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_from, senha)
        smtp.send_message(msg)


if __name__ == "__main__":
    send_email_with_csv("imoveis_comerciais.csv")
