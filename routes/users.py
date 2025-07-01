from fastapi import APIRouter, HTTPException, status, Depends
from models.users import User, UserSingIn
from sqlmodel import select
from database.connection import get_session
from auth.hashing import hash_password, verify_password
from auth.jwt_handler import create_access_token
from auth.jwt_bearer import JWTBearer

# User 담당 라우터 
user_router = APIRouter(
    tags = ['User']
)

# users = {}

# 회원가입 라우터 
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
    
    data.password = hash_password(data.password) # 회원가입시 비밀번호 해싱 
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
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User dose not exist"
        )
    # 리펙토링 
    # 현재 평문 비밀번호 비교이므로, 해시 방식으로 변경 
    # if db_user.password != user.password:
    #     raise HTTPException(
    #         status_code = status.HTTP_403_FORBIDDEN,
    #         detail = "Wrong credentials passed"
    #     )
    token = create_access_token({'sub':db_user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "message":"User signed in successfully"
    }

     
@user_router.get("/profile", dependencies=[Depends(JWTBearer())])
async def read_profile():
    return {"message": "You are authenticated"}