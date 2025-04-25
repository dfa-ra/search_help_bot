from dataclasses import dataclass
from typing import Optional

from bson import Binary


@dataclass
class FileModel:
    file_name: Optional[str]
    file_bytes: Optional[Binary]
    mime_type: Optional[str]
