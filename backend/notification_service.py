import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path


DEFAULT_NOTIFY_EMAIL = "eleftherioskaram@gmail.com"
LOG_PATH = Path(__file__).with_name("notifications.log")


def notify_schedule_changed(action, details=""):
    recipient = os.environ.get("ORAR_NOTIFY_EMAIL", DEFAULT_NOTIFY_EMAIL)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"[Orar Licenta] Orar modificat: {action}"
    body = (
        f"Orarul a fost modificat.\n\n"
        f"Actiune: {action}\n"
        f"Detalii: {details or '-'}\n"
        f"Data: {timestamp}\n"
    )

    host = os.environ.get("ORAR_SMTP_HOST", "").strip()
    user = os.environ.get("ORAR_SMTP_USER", "").strip()
    password = os.environ.get("ORAR_SMTP_PASSWORD", "").strip()
    sender = os.environ.get("ORAR_SMTP_FROM", user or recipient).strip()
    port = int(os.environ.get("ORAR_SMTP_PORT", "587"))
    use_tls = os.environ.get("ORAR_SMTP_TLS", "1") != "0"

    if not host or not user or not password:
        _write_log(timestamp, recipient, subject, body, "SMTP neconfigurat")
        return {"sent": False, "reason": "SMTP neconfigurat"}

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            if use_tls:
                server.starttls()
            server.login(user, password)
            server.send_message(message)
        return {"sent": True, "reason": "Email trimis"}
    except Exception as error:
        _write_log(timestamp, recipient, subject, body, f"Eroare SMTP: {error}")
        return {"sent": False, "reason": str(error)}


def _write_log(timestamp, recipient, subject, body, status):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write("=" * 72 + "\n")
        log_file.write(f"Status: {status}\n")
        log_file.write(f"Catre: {recipient}\n")
        log_file.write(f"Subiect: {subject}\n")
        log_file.write(f"Data: {timestamp}\n\n")
        log_file.write(body)
        log_file.write("\n")
