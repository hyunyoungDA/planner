from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

database_file = "planner.db"
# 현재 프로젝트 폴더에 planner.db라는 SQLite 폴더 생성
database_connection_string = f"sqlite:///{database_file}"

# Fastapi는 여러 스레드를 이용 -> False로 오류 처리 
connect_args = {"check_same_thread": False}

# SQLAlchemy의 엔진 객체 생성 
engine_url = create_engine(database_connection_string, echo = True,\
    connect_args = connect_args)

# db 생성 함수 
def conn():
    SQLModel.metadata.create_all(engine_url)

# 요청마다 안전하게 세션을 열고 닫도록 만드는 의존성 세션 함수
# 요청이 끝나면 세션을 안전하게 종료 
def get_session():
    with Session(engine_url) as session:
        yield session # 요청이 생기면 한 번만 실행
        