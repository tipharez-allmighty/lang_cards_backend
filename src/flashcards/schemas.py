from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class ImageBase(BaseModel):
    id: UUID
    url: str
    
    class Config:
        from_attributes = True

class WordBase(BaseModel):
    id: UUID
    word: str
    image: ImageBase
    
    class Config:
        from_attributes = True

class FlashCardBase(BaseModel):
    id: UUID
    native_lang: str
    target_lang: str
    data: dict
    created_at: datetime
    word: WordBase
    
    class Config:
        from_attributes = True