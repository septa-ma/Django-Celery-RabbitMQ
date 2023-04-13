from django.template import Context
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage

def send_suggestion_email(name, email, suggestion):
    context = {
        'name': name,
        'email': email,
        'suggestion': suggestion,
    }
    email_subject = 'thanks for your suggestion.'
    email_body = render_to_string('email.message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)