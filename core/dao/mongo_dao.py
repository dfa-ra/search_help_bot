from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from core.models import FileModel


class MongoDao:
    """класс для взаимодействия с монго дб"""
    def __init__(self, collection):
        self.collection = collection

    # сохранения файла
    async def save_file(self, file: FileModel):

        result = await self.collection.insert_one({
            "file_name": file.file_name,
            "mime_type": file.mime_type,
            "file_bytes": file.file_bytes
        })
        return str(result.inserted_id)

    # получение файла из бд
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
