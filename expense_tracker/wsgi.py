import os
from django.core.wsgi import get_wsgi_application



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')

# Load Django
application = get_wsgi_application()

# Initialize MongoDB AFTER Django loads
# MongoDB init
from api.mongo import init_mongo
init_mongo()
