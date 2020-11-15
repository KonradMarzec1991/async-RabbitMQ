"""
Module contains project variables
"""

DB_NAME = 'pair.db'

CELERY_NAME = 'receiver'
CELERY_BACKEND = 'rpc://'
CELERY_BROKER = 'pyamqp://guest@localhost//'
