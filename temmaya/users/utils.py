from .models import User
import random
from django.core.mail import EmailMessage
from temmaya.settings import EMAIL_HOST_USER

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def username_generator(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return username_generator(random_username)
    

def email_sender(email, title, body):

    message = EmailMessage(
        title, body, EMAIL_HOST_USER, [email,'fayyoz1@mail.ru'])
    message.send()
    return "DONE!"

def email_by_template(subject, ctx, template_path, to=[]):
    # Load the HTML template
    html_template = get_template(template_path)
    
    # Populate the template with data from the context dictionary
    html_content = html_template.render(ctx)
    
    # Create the email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(html_content),  # Use the plain text version as fallback
        from_email=EMAIL_HOST_USER,
        to=to
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    # Attach the HTML content