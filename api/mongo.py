import os
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if MONGO_URI :
    connect(host = MONGO_URI)

else :
    connect("expense_db")
 
