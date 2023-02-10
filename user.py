from config import database

user_collection = database.client["exceed06"]["user"]

user_collection.delete_many({})
