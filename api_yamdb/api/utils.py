import random

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from reviews.models import User


def confirmation_generator(username):
    '''Generate confirmation codes'''

    user = get_object_or_404(User, username=username)
    confirmation_code = ''.join(
        [random.choice(settings.CONF_GEN) for x in range(15)]
    )
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        settings.MAIL_SUBJECT,
        confirmation_code,
        settings.FROM_EMAIL,
        [user.email],
        fail_silently=False
    )
