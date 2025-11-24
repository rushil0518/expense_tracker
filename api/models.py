from django.db import models
from mongoengine import Document, StringField, DateTimeField, FloatField, ListField
from datetime import datetime

# Create your models here.

class Category(Document) :
    meta = {'collection' : 'categories'}

    name = StringField(required = True)
    user_id = StringField(default = None, Null = True)
    color = StringField(default = "4BC0C0")
    icon = StringField(default = "")
    created_at = DateTimeField(default = datetime.utcnow)

    def __str__(self):
      return f"{self.name} ({self.user_id})"

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "user_id": self.user_id,
            "color": self.color,
            "icon": self.icon
        }
   
class Expense(Document):
    meta = {'collection': 'expenses'}

    user_id = StringField(required=True)
    category = StringField(required=True)
    amount = FloatField(required=True, min_value=0)
    date = DateTimeField(default=datetime.utcnow)
    note = StringField(default="")
    tags = ListField(StringField())
    created_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "category": self.category,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "note": self.note,
            "tags": self.tags
        }
    
# class Budget(Document):
#     meta = {'collection': 'budgets'}

#     user_id = StringField(required=True)
#     category = StringField(required=False)
#     limit = FloatField(required=True, min_value=0)
#     month = StringField(required=True)  # Example: 
#     created_at = DateTimeField(default=datetime.utcnow)

#     def to_dict(self):
#         return {
#             "id": str(self.id),
#             "user_id": self.user_id,
#             "category": self.category,
#             "limit": self.limit,
#             "month": self.month
#         }

class Budget(Document):
    meta = {'collection': 'budgets'}

    user_id = StringField(required=True)
    amount = FloatField(required=True, min_value=0)
    month = StringField(required=True)  # "2025-11"
    created_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "amount": self.amount,
            "month": self.month
        }