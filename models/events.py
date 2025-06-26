from sqlmodel import JSON, SQLModel, Field, Column, Relationship
# from models.users import User
from typing import List, Optional, TYPE_CHECKING

# 순환 참조 오류 방지 
if TYPE_CHECKING:
    from models.users import User

class Event(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column = Column(JSON)) #tags를 JSON형식으로 db에 저장 
    location: str
    
    user_id: Optional[int] = Field(default = None, foreign_key = "user.id")
    user: Optional["User"] = Relationship(back_populates="events")
    
    # 현재는 class Config 말고 model_config = 형식을 사용함, pydantic v2 
    model_config = {
        "arbitrary_types_allowed": True, # JSON이나 사용자 정의 타입 허용 
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book",
                "tags": ["Python", "fastapi", "django", "launch"],
                "location": "Google Meet"
            }
        }
    }
    
# 이벤트 업데이트 스키마
class EventUpdate(SQLModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book",
                "tags": ["Python", "fastapi", "django", "launch"],
                "location": "Google Meet"
            }
        }
    }