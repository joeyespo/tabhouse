"""\
Helper.py

Helper functions for the current Flask web application.
"""

import os
import logging
from logging.handlers import SMTPHandler
from flask import url_for, current_app


def try_parse_int(s, default_value=None):
    """Parse an integer or return a default value if it cannot be done."""
    try:
        return int(s)
    except ValueError:
        return default_value


def add_jinja_helpers(app):
    """Adds helper globals to jinja."""
    # Static file helpers
    app.jinja_env.globals.update(static_for=static_for)


def static_for(filename, endpoint='.static'):
    """Provides the 'static' function that also appends the file's timestamp to the URL, usable in a template."""
    return url_for(endpoint, filename=filename) + '?' + str(int(os.path.getmtime(os.path.join(current_app.static_folder, filename))))


def email_errors(app, email_info=None, error_level=logging.ERROR):
    """Enables error reporting using SMTP for the provided app."""
    if not email_info:
        email_info = app.config.get('ERROR_EMAIL_INFO')
    if not email_info:
        return
    mailhost, from_address, to_addresses, subject, credentials = email_info
    mail_handler = TlsSMTPHandler(mailhost, from_address, to_addresses, subject, credentials)
    if error_level:
        mail_handler.setLevel(error_level)
    app.logger.addHandler(mail_handler)


class TlsSMTPHandler(SMTPHandler):
    """A TLS implementation of SMTPHandler."""
    
    def emit(self, record):
        """
        Emit a record.
        
        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            import string
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport or smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (self.fromaddr, string.join(self.toaddrs, ","), self.getSubject(record), formatdate(), msg)
            # --- Begin TLS support ---
            if self.username:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(self.username, self.password)
            # --- End TLS support ---
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
