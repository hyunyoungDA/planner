from passlib.context import CryptContext 

# 암호화 컨텍스트 객체 
# deprecated = 'auto': 스키마 변경 시 자동 감지 
pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

def hash_password(password: str) -> str:
  """
  사용자에게서 입력 받은 평문 비밀번호를 bcrypt 알고리즘을 통해 해시된 비밀번호 반환 
  Args:
      password (str): 사용자가 입력한 비밀번호 

  Returns:
      _type_: 해싱된 비밀번호 
  """
  return pwd_context.hash(password)

# 비밀번호 검증 
def verify_password(plain_password: str, hashed_password: str):
  """
  사용자가 로그인할 때 입력한 평문 비밀번호가 이미 저장된 해시와 일치하는지 확인하는 함수
  Args:
      plain_password (str): 사용자가 입력한 평문 비밀번호
      hashed_password (str): 이미 저장된 해시 비밀번호 

  Returns:
      _type_: 비밀번호가 일치하면 True, 그렇지 않으면 False
  """
  return pwd_context.verify(plain_password, hashed_password)