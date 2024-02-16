import pymongo
import os
import sys

class Database():
    def __init__(self):
      self.client: pymongo.MongoClient = None
  
    def connect_to_DB(self):
      try:
        self.client = pymongo.MongoClient(os.environ.get('DB_TOKEN'))
      except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)

    def send_to_DB(self, file):
      try:
        db = self.client.Cluster0
        my_collection = db["feedback"]
        result = my_collection.insert_one(file)
      except pymongo.errors.OperationFailure:
          print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
          sys.exit(1)
      else:
          print(f"I inserted {result} document")


