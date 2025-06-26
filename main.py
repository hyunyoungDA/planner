from fastapi import FastAPI, Request
from routes.users import user_router
from routes.events import event_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from database.connection import conn
import uvicorn 

# Lifespan 역시 app에 등록해야 사용할 수 있음
# DB 연동시 async로 비동기 처리 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 실행시
    print("DB 생성 및 연결 시작")
    conn()
    yield
    # 앱 종료시 실행될 코드 작성 
    print("앱 종료 시 정리")

app = FastAPI(lifespan = lifespan)

# CSS, JS 등을 서빙 
app.mount("/static", StaticFiles(directory='static'), name = 'static')\
    
# Jinja2 템플릿 설정 
templates = Jinja2Templates(directory = 'templates')

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

# 라우터를 app에 등록해야지만 사용할 수 있음 
app.include_router(user_router, prefix="/users")
app.include_router(event_router, prefix = "/events")

if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000,\
        reload = True)