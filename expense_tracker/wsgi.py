import os
from django.core.wsgi import get_wsgi_application

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')

# Connect to Mongo BEFORE Django loads
from api.mongo import init_mongo
init_mongo()

# Now load Django
application = get_wsgi_application()

