import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import jinja2
from dotenv import load_dotenv

from Error_Handler.Logger import Logger
from Utils.dates import get_date_today, get_last_week_date, convert_month_day_string

load_dotenv()

sender_email = os.getenv("SENDER_MAIL")
sender_password = os.getenv("SENDER_EMAIL_PASSWORD")
mail_server = os.getenv("MAIL_SERVER")
mail_port = os.getenv("MAIL_PORT")


def send_mail(data, receiver_mail):
    logger = Logger('mail_log',
                    './Logs/mail.log',
                    '%(asctime)s. %(levelname)s. %(message)s')

    subject = (f'Weekly Station Status Report ({convert_month_day_string(get_last_week_date())}) - '
               f'({convert_month_day_string(get_date_today())})')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_mail
    msg['Subject'] = subject

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('Features/Mailer/templates'))
    template = env.get_template('template_outlook_v3.html')
    rendered_html = template.render(data=data)
    html_body = MIMEText(rendered_html, 'html')
    msg.attach(html_body)

    smtp_server = mail_server
    smtp_port = 465

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as connection:
            # server.starttls()
            connection.login(sender_email, sender_password)
            response = connection.sendmail(msg['From'], msg['To'], msg.as_string())
            return response
    except Exception as e:
        logger.write_log(level=40, message=f'An exception caught. {e}')
