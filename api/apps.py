from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import api.mongo
        # Avoid circular imports by importing inside method
        from .utils import preload_default_categories
        

        try:
            preload_default_categories()
        except Exception as e:
            # During migrations or startup, DB might not be ready
            print("Skipping category preload:", e)
