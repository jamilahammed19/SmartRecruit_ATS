import os
from celery import Celery

# Define the default Django settings module so Celery knows where to find our configurations
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sr_ats.settings')

# Initialize the Celery application specifically for our ATS
app = Celery('sr_ats')

# Read configuration from Django settings, looking specifically for variables starting with "CELERY_"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically look through all installed Django apps (like notifications) for a tasks.py file
app.autodiscover_tasks()