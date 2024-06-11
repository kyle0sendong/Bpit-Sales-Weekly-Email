import flask
import json
from flask_mail import Mail, Message
import jinja2
import os
from dotenv import load_dotenv

load_dotenv()

sender_mail = os.getenv("SENDER_MAIL")
sender_password = os.getenv("SENDER_EMAIL_PASSWORD")
mail_server = os.getenv("MAIL_SERVER")
mail_port = os.getenv("MAIL_PORT")

test_email1 = os.getenv("TEST_EMAIL1")

app = flask.Flask(__name__, template_folder='./templates')
app.config.update(dict(
    MAIL_USERNAME=sender_mail,
    MAIL_PASSWORD=sender_password,
    MAIL_SERVER=mail_server,
    MAIL_PORT=mail_port,
    MAIL_USE_TLS=True
))
mail = Mail(app)


# For testing purposes
@app.route('/')
def view_mail():
    with open("../../Data/mailer_data.json", "r") as f:
        json_data = json.load(f)

    rendered_html = flask.render_template('template_outlook_v2_no_parameters.html', data=json_data[0])
    return rendered_html


@app.route('/send-mail')
def send_mail():
    with open("../../Data/mailer_data.json", "r") as f:
        json_data = json.load(f)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    template = env.get_template("template_outlook_v2_no_parameters.html")
    rendered_html = template.render(data=json_data[0])
    msg = Message(
        subject="Test mail",
        sender=sender_mail,
        recipients=[test_email1]
    )
    msg.html = rendered_html
    mail.send(msg)
    return "e-mail sent"


app.run(debug=True)
