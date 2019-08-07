#


# from celery import Celery
#
# celery_app = Celery('celery_app', include=['celery_app.celery'])
# celery_app.config_from_object('celery_app.celeryconfig') #导入配置
# # Optional configuration, see the application user guide.
# celery_app.conf.update(
#     result_expires=3600,
# )


from celery import Celery

c = Celery('mails')
c.config_from_object('celery_app.celeryconfig')
# c.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'celery_app.pfc.send_mail',
#         'schedule': 30.0
#
#     },
# }
