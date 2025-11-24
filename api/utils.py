from .models import Category

DEFAULT_CATEGORIES = [
    {"name": "Food", "color": "#FF9F40"},
    {"name": "Transport", "color": "#36A2EB"},
    {"name": "Shopping", "color": "#FF6384"},
    {"name": "Entertainment", "color": "#9966FF"},
    {"name": "Education", "color": "#FFCD56"},
    {"name": "Health", "color": "#4BC0C0"},
    {"name": "Bills", "color": "#C9CBCF"},
]

def preload_default_categories():
    for cat in DEFAULT_CATEGORIES:
        exists = Category.objects(name=cat["name"], user_id=None).first()
        if not exists:
            Category(name=cat["name"], user_id=None, color=cat["color"]).save()