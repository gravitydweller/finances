#pools/apps.py

from django.apps import AppConfig


class PoolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pools'

    def ready(self):
        import pools.signals  # This ensures signals are connected when the app is ready
