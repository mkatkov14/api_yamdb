import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from reviews.models import User

CONF_GEN = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'


def confirmation_generator(username):
    '''Generate confirmation codes'''

    user = get_object_or_404(User, username=username)
    confirmation_code = ''.join([random.choice(CONF_GEN) for x in range(15)])
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        'Код подтверждения регистрации',
        confirmation_code,
        'yamdb.host@yandex.ru',
        [user.email],
        fail_silently=False
    )
