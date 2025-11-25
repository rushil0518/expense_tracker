import os
from dotenv import load_dotenv
from mongoengine import connect

def init_mongo():
    load_dotenv()

    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        print("⚠ No MONGO_URI found in environment — using local DB")
        connect("expense_db", alias="default")
        return

    print("✔ Connecting to MongoDB Atlas...")
    connect(host=MONGO_URI, alias="default")
