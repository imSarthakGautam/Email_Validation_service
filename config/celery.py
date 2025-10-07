
import os
from celery import Celery
# Celery: main class from Celery package to create a new Celery app instance

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Celery needs to know where default django settings are 
# setdefault() helps to use same env varibles


celery_app = Celery('config') 
# celery app instance, which will be used by workers

celery_app.config_from_object('django.conf:settings', namespace='CELERY') 
# celery loads configurations from settings.py
# settings begining with 'CELERY'

celery_app.autodiscover_tasks()
# tells to autodiscover tasks from Django Apps
# looks for tasks.py inside each apps listed in INSTALLED_APPS


@celery_app.task(bind=True)
def debug_task(self):
    """
    defines taks that prints full details of task request
    """
    print(f'Request: {self.request!r}')