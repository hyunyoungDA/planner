#from pydantic import BaseModel, EmailStr
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING 

# User에서 Event 참조 해야됨
# 순환 참조 방지 
if TYPE_CHECKING:
    from models.events import Event # 타입 검사용이므로 실행 시 import 안 됨 

class User(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key=True)
    email: EmailStr = Field(unique = True, index = True, nullable = False)
    password: str
    # username: str
    # user와 events 간의 관계 설정 
    events: List["Event"] = Relationship(back_populates = 'user')
    
    model_config = {
        "json_schema_extra":{
            "example":{
                "email":"fastapi@spark.com",
                "password":"strong!!",
                "events":[],
            }
        }
    }
        
        
class UserSingIn(SQLModel):
    email: EmailStr
    password: str
    
    model_config = {
        "json_schema_extra":{
            "example":{
                "email":"fastapi@spark.com",
                "password":"strong!!",
                "events":[],
            }
        }
    }