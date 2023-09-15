from django.apps import AppConfig

# I wrote this code -------------------------- Start
class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # Import the signals modules
        import myapp.signals  
# I wrote this code -------------------------- End