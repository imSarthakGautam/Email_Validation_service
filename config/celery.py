import os
from celery import Celery

# Point to the correct settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
# Or use 'config.settings.local' or 'config.settings.production' depending on your environment

celery_app = Celery('config') 

# Load configurations from Django settings with CELERY_ prefix
celery_app.config_from_object('django.conf:settings', namespace='CELERY') 

# Autodiscover tasks
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
    """
    Defines task that prints full details of task request
    """
    print(f'Request: {self.request!r}')