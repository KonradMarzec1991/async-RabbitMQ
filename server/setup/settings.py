"""
Module contains project variables
"""
import os

DB_NAME = os.getenv('DB')

CELERY_NAME = 'receiver'
CELERY_BACKEND = 'rpc://'
CELERY_BROKER = 'pyamqp://guest@rabbitmq//'
