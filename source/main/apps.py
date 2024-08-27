from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

# realtors/apps.py
def ready(self):
    import main.signals
