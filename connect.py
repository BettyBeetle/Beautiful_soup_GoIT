from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

def connect_to_mongodb():
    try:
        client = MongoClient(f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority")
        db = client[db_name]
        return db
    except Exception as e:
        print("Error connecting to MongoDB Atlas:", e)
        return None
