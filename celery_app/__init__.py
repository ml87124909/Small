#

from celery import Celery

c = Celery('mails')
c.config_from_object('celery_app.celeryconfig')
