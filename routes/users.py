from fastapi import APIRouter, HTTPException, status, Depends
from models.users import User, UserSingIn
from sqlmodel import select
from database.connection import get_session

# User 담당 라우터 
user_router = APIRouter(
    tags = ['User']
)

# users = {}

# 사용자 등록 라우트
@user_router.post("/signup")
async def sign_new_user(data: User, session = Depends(get_session)) -> dict:
    users = select(User).where(User.email == data.email) # User 객체의 이메일과 받은 data의 이메일 비교 
    result = session.exec(users).first() # 가장 첫 번째 행만 가져옴 
    
    # 이미 존재하는 경우 
    if result:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with supplied username exists"
        )
        
    session.add(data)
    session.commit()
    session.refresh(data)
    
    return{
        "message":"User successfully registered!"
    }

# 사용자 로그인 라우터 
@user_router.post("/signin")
async def sign_user_in(user: UserSingIn, session = Depends(get_session)) -> dict:
    statement = select(User).where(User.email == user.email)
    
    db_user = session.exec(statement).first()
    
    if not db_user:
        
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User dose not exist"
        )
    if db_user.password != user.password:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Wrong credentials passed"
        )
    return {
        "message":"User signed in successfully"
    }
    
    