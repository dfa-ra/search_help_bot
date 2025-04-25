import asyncio
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


async def check_connection():
    try:
        server_info = await client.server_info()
        print("MongoDB connection successful. Server info:", server_info)
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


async def check_collection():
    try:
        document = await files_collection.find_one()
        if document:
            print("Документ найден:", document)
        else:
            print("Коллекция пуста.")
    except Exception as e:
        print(f"Ошибка при поиске в коллекции: {e}")


async def main():
    await check_connection()
    await check_collection()

if __name__ == "__main__":
    asyncio.run(main())
