from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    name = 'notifications'
    default_auto_field = 'django.db.models.BigAutoField'

    # The ready method fires automatically when Django boots up this specific app.
    # We import our signals here so Django's event dispatcher starts listening for them immediately.
    def ready(self):
        import notifications.signals