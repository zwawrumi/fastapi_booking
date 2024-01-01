import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.tasks.celery import celery_app
from app.tasks.email_task import confirmation_booking
from config import settings


@celery_app.task
def process_img(
        path: str
):
    img_path = Path(path)
    img_open = Image.open(img_path)
    img_resize_big = img_open.resize((1000, 500))
    img_resize_small = img_open.resize((200, 100))
    img_resize_big.save(f'app/static/images/resized_1000_500_{img_path.name}')
    img_resize_small.save(f'app/static/images/resized_200_100_{img_path.name}')


@celery_app.task
def send_confirmation_email(booking: dict, email: EmailStr):
    email_to_send = settings.EMAIL
    msg_content = confirmation_booking(booking, email_to_send)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.EMAIL, settings.GM_PASS)
        server.send_message(msg_content)