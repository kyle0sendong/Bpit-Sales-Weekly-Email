import smtplib
import jinja2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from Utils.dates import get_date_today, get_last_week_date, convert_month_day_string
from Logs.logger import logger


load_dotenv()

sender_email = os.getenv("SENDER_MAIL")
sender_password = os.getenv("SENDER_EMAIL_PASSWORD")
mail_server = os.getenv("MAIL_SERVER")
mail_port = os.getenv("MAIL_PORT")


def create_log(level, message):
    execution_logger = logger('mail_log',
                              './Logs/mail.log',
                              '%(levelname)s. %(message)s %(asctime)s')

    execution_logger.write_log(level=level, message=message)


def send_mail(data, receiver_mail):

    subject = (f'Weekly Status Report ({convert_month_day_string(get_last_week_date())}) - '
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
    smtp_port = int(mail_port)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            response = server.sendmail(msg['From'], msg['To'], msg.as_string())
            return response
    except Exception as e:
        create_log(40, f'{e}')

