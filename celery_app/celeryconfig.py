## -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) wxmall.janedao.cn
# Author：QQ173782910
#QQ group:528289471
##############################################################################
"""celery_app/celeryconfig.py"""

from datetime import timedelta
from celery.schedules import crontab

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'

# Timezone
CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

# import
CELERY_IMPORTS = (
    'celery_app.pfc',
    'celery_app.db_backup',
)

# schedules
CELERYBEAT_SCHEDULE = {
    'every-120-seconds': {
        'task': 'celery_app.pfc.update_order',
        'schedule': 120.0,
    },
    'every-100-seconds': {
        'task': 'celery_app.pfc.update_pt',
        'schedule': 100.0,
    },
    'every-600-seconds': {
        'task': 'celery_app.pfc.update_refund',
        'schedule': 180.0,
    },
    'backup_db' : {
        'task': 'celery_app.db_backup.backup_db',
        'schedule': crontab(minute=37, hour=3),  # 每天早上 3 点 30 分执行一次
    },
    'Did_not_pay' : {
        'task' : 'celery_app.pfc.Did_not_pay',
         'schedule': crontab(minute=37,hour=1),  # 每天早上 1 点 30 分执行一次
    },
    'Did_not_oss': {
        'task': 'celery_app.pfc.Did_not_oss',
        'schedule': crontab(minute=37, hour=0),  # 每天早上 0 点 30 分执行一次
    },
    'every-70-seconds': {
        'task': 'celery_app.pfc.money_pay',
        'schedule': 70.0,
    },
# 'multiply-at-some-time': {
    #     'task': 'celery_app.celery.send_mail_0',
    #     'schedule': crontab(hour=0, minute=30),  # 每天早上 0 点 50 分执行一次
    #    'args': ()                               # 任务函数参数
    # },
    # 'multiply-at-time': {
    #     'task': 'celery_app.celery.send_mail_13',
    #     'schedule': crontab(hour=13, minute=30),  # 每天早上 13 点 50 分执行一次
    #    'args': ()                               # 任务函数参数
    # }
}

