from django.template.loader import render_to_string, get_template
from send_message.celery import app
from django.core.mail import send_mail, EmailMessage
from send_message.settings import EMAIL_HOST_USER
from .models import User

@app.task
def send_registration_mail(user_email, subscription):
    """
    Sending a registration letter
    """
    send_mail(
        'Thank you for registering',
        'You have subscribed to the newsletter {0}'.format(subscription),
        EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )


@app.task
def send_subscribed_mail(user_email, user_name, subscription):
    """
    Sending a subscription notification
    """
    send_mail(
        'Hello dear {0}'.format(user_name),
        'You subscribed from the news {0}'.format(subscription),
        EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )

@app.task
def send_unsubscribed_mail(user_email, user_name, subscription):
    """
    Sending an unsubscribe notification
    """
    send_mail(
        'Hello dear {0}'.format(user_name),
        'You unsubscribed from the news {0}'.format(subscription),
        EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )


@app.task
def send_hb_email(template, subject, email, context):
    html_msg = get_template(template).render(context)
    msg = EmailMessage(subject, html_msg, to=(email, ), from_email=EMAIL_HOST_USER)
    msg.content_subtype = 'html'
    msg.send()



@app.task
def send_subs_email(template, subject, email, context):
    html_msg = get_template(template).render(context)
    msg = EmailMessage(subject, html_msg, to=(email,), from_email=EMAIL_HOST_USER)
    msg.content_subtype = 'html'
    msg.send()