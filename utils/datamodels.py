import logging
from flask_mail import Message
from traceback import format_exc
from flask import request
from server.utils import secrets

class MailLogHandler(logging.Handler):

    def __init__(self, mail):
        self.mail = mail
        logging.Handler.__init__(self)

    def flush(self):
        pass

    def emit(self, record):
        msg = Message(
                'Instapizza Instabummer',
                sender=secrets.MAIL_USERNAME,
                recipients = [secrets.TEAM_EMAIL])
        msg.body = "Request:\n"
        msg.body += "%s: %s\n" % (request.method, request.url)
        msg.body += "FORM: %s\n" % filter(lambda item: item[0] != 'password', request.form.items())
        msg.body += "ARGS: %s\n" % filter(lambda item: item[0] != 'password', request.args.items())
        msg.body += '\n'
        msg.body += format_exc()
        print msg.body
        self.mail.send(msg)
