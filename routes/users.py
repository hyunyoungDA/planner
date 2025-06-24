from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSingIn

user_router = APIRouter(
    tags = ['User']
)

users = {}

# 등록 라우트, 기존에 users에 이미 존재하는 email이라면 예외처리 
@user_router.post("/signup")
async def sign_new_user(data: User) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with supplied username exists"
        )
    users[data.email] = data
    return{
        "message":"User successfully registered!"
    }

# 사용자 로그인 라우터 
@user_router.post("/signin")
async def sign_user_in(user: UserSingIn) -> dict:
    if user.email not in users:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User dose not exist"
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Wrong credentials passed"
        )
    return {
        "message":"User signed in successfully"
    }
    
    