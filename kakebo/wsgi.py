"""
WSGI config for kakebo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#add-start yama
from whitenoise.django import DjangoWhiteNoise
#add-end yama

#del-start yama
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kakebo.settings")
#del-end yama

application = get_wsgi_application()
#add-start yama
application = DjangoWhiteNoise(application)
#add-end yama
