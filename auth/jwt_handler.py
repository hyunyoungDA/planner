from datetime import datetime, timedelta
from jose import jwt 

# 보통 .env에서 관리 
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256" # sign 알고리즘으로, 일반적으로 HS256 사용 
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 토큰 만료 시간 

def create_access_token(data: dict, expires_delta: timedelta = None):
  """
  사용자 정보를 기반으로 JWT 엑세스 토큰 생성 함수 

  Args:
      data (dict): 토큰에 담길 사용자 데이터 (예: {"sub":user.email})
      expires_delta (timedelta, optional): 토큰 만료 시간, default = 30m
      
  Returns:
      str: 생성된 JWT 액세스 토큰
  """
  
  to_encode = data.copy()
  expire = datetime.utcnow() + (expires_delta or timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES))
  to_encode.update({'exp':expire})
  
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt