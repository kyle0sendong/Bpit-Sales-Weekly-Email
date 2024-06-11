import smtplib
import jinja2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("SENDER_MAIL")
sender_password = os.getenv("SENDER_EMAIL_PASSWORD")
mail_server = os.getenv("MAIL_SERVER")
mail_port = os.getenv("MAIL_PORT")


def send_mail(data, receiver_mail):

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_mail
        msg['Subject'] = 'Test1'

        env = jinja2.Environment(loader=jinja2.FileSystemLoader('Features/Mailer/templates'))
        template = env.get_template('template_outlook_v2_no_parameters.html')
        rendered_html = template.render(data=data)
        html_body = MIMEText(rendered_html, 'html')
        msg.attach(html_body)

        smtp_server = mail_server
        smtp_port = int(mail_port)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            return server.sendmail(msg['From'], msg['To'], msg.as_string())

    except Exception as e:
        print(e)
        return


