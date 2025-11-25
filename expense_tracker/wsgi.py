import os
from django.core.wsgi import get_wsgi_application

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')



# Now load Django
application = get_wsgi_application()

