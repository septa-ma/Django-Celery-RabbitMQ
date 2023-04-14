# 4- create email.py for email configuration that can be send.
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_suggestion_email(name, email, suggestion):
    context = {
        'name': name,
        'email': email,
        'suggestion': suggestion,
    }
    subject = 'thanks for your suggestion.'
    # 5- create email_message.txt for saving email content.
    body = render_to_string('email_message.txt', context)

    # use EmailMessage class for sending an email to a user.
    emailMsg = EmailMessage(
        subject, body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return emailMsg.send(fail_silently=False)