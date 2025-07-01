from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from jose import jwt, JWTError

from auth.jwt_handler import SECRET_KEY, ALGORITHM

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization")

        token = credentials.credentials
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload  # 필요한 경우 return payload["sub"]
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid or expired token")