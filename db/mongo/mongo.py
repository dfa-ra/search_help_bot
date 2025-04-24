import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(dotenv_path="/media/ra/_work/ra/QUESTIONABLE PROJECTS/help_search_bot/.env")

mongo_url = os.getenv("MONGO_DB_URL")
mongo_name_db = os.getenv("MONGO_DB_NAME")
mongo_name_collection = os.getenv("MONGO_NAME_COLLECTION")

client = AsyncIOMotorClient(mongo_url)
db = client[mongo_name_db]
files_collection = db[mongo_name_collection]