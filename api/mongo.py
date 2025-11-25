import os
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

def init_mongo():
    MONGO_URI = os.getenv("MONGO_URI")

    if MONGO_URI:
        connect(host=MONGO_URI, alias="default")
    else:
        connect("expense_db", alias="default")
