from email.message import EmailMessage

from pydantic import EmailStr

from config import settings


def confirmation_booking(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()
    email['Subject'] = 'Confirm booking'
    email['From'] = settings.EMAIL
    email['To'] = email_to

    email.set_content(
        f'''
        <h1>Confirm booking</h1> 
        You have booked a hotel from {booking['date_from']} to {booking['date_to']}
        ''',
        subtype='html'
    )
    return email
