# This guarantees that the Celery app is loaded the moment Django starts.
# Without this, Django would not know how to pass tasks to the Redis broker.
from .celery import app as celery_app

__all__ = ('celery_app',)