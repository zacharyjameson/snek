import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

mongodb_password = os.getenv("MONGODB_PASSWORD")
mongodb_user = os.getenv("MONGODB_USER")


def get_database():
    CONNECTION_STRING = f"mongodb+srv://{mongodb_user}:{
        mongodb_password}@khazaddum.vcmwm7d.mongodb.net/?retryWrites=true&w=majority"

    print("Connecting to MongoDB with URI:", CONNECTION_STRING)

    # Create a new client and connect to the server
    client = MongoClient(CONNECTION_STRING)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client.Snake
    except Exception as e:
        print("Error connecting to MongoDB:", e)


if __name__ == "__main__":
    db = get_database()
