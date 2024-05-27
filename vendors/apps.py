# from django.apps import AppConfig


# class VendorsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'vendors'



from django.apps import AppConfig

class VendorsConfig(AppConfig):
    name = 'vendors'

    def ready(self):
        import vendors.signals  # This will register the signals
