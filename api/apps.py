from django.apps import AppConfig
import threading
import time

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Delayed preload so DB is ready
        def delayed_preload():
            time.sleep(5)  # wait for Mongo to fully connect
            try:
                from .utils import preload_default_categories
                preload_default_categories()
                print("✔ Default categories preloaded")
            except Exception as e:
                print("⚠ Could not preload categories:", e)

        threading.Thread(target=delayed_preload).start()