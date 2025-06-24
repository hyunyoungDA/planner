from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models.events import Event # User에서 Event 참조 해야됨

class User(BaseModel):
    email: EmailStr
    password: str
    # username: str
    events: Optional[List[Event]] # Event 모델을 받음 
    
    class Config:
        schema_extra = {
            "example":{
                "email":"fastapi@spark.com",
                "password":"strong!!",
                "events":[],
            }
        }
        
class UserSingIn(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example":{
                "email":"fastapi@spark.com",
                "password":"strong!!",
                "events":[],
            }
        }