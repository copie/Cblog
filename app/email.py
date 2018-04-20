from threading import Thread

from flask import copy_current_request_context, current_app, render_template
from flask_mail import Message

from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, ** kwarges):
    app = current_app._get_current_object()
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX']+subject,
                  sender=current_app.config['MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template+'.txt', **kwarges)
    msg.html = render_template(template+'.html', **kwarges)
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
    return thr
