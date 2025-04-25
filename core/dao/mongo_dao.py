from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from core.models import FileModel


class MongoDao:
    def __init__(self, collection):
        self.collection = collection

    async def save_file(self, file_name, mime_type, file_bytes):
        result = await self.collection.insert_one({
            "file_name": file_name,
            "mime_type": mime_type,
            "file_bytes": file_bytes
        })
        return str(result.inserted_id)

    async def get_file(self, file_id):
        try:
            file_doc = await self.collection.find_one({"_id": ObjectId(file_id)})
            file = FileModel(
                file_name=file_doc["file_name"],
                file_bytes=file_doc["file_bytes"],
                mime_type=file_doc["mime_type"]
            )
            if file_doc:
                print("return FILEEEEE")
                return file
            print("PPUPUPUPUPU")
        except Exception as e:
            print("PPUPUPUPUPU2222")
            raise Exception(e)
