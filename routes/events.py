from fastapi import APIRouter, HTTPException, status, Depends, Request
from database.connection import get_session # 세션 불러오기 
from models.events import Event, EventUpdate
from sqlmodel import select 
from typing import List

# tags: 해당 라우터가 담당하는 API그룹에 대한 태그 이름 지정 
event_router = APIRouter(
    tags = ["Events"]
)

# 임시 DB 역할 
# events = []

# 모든 이벤트 추출
@event_router.get("/", response_model = List[Event]) # 출력 형식 지정; Event 객체가 담긴 리스트 형태로 응답이 올 것. 
# Depends: 의존성 주입 -> Fastapi가 알아서 get_session을 생성해서 session 인자로 넘겨줌 
async def retrieve_all_events(session = Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events

# 특정 ID의 이벤트 추출 라우터
@event_router.get("/{id}", response_model = Event)
async def retrieve_event(id: int, session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Event with supplied ID dose not exist."
    )

# 새로운 event 업로드 라우터 
@event_router.post("/new")
async def create_event(new_event: Event, session = Depends(get_session)) -> dict:
    session.add(new_event) # 세션에 pending 상태로 등록됨. 
    session.commit() # 변경사항을 실제 DB에 저장 
    session.refresh(new_event) # 자동으로 채워지지 않은 값을 불러와서 저장 
    
    return{
        "message":"Event created successfully."
    }

# 삭제 라우터     
@event_router.delete("/{id}")
async def delete_event(id: int, session = Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
            
        return{
            "Message":"Event deleted successfully."
        }
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Event with supplied ID dose not exist"
    )
    
@event_router.delete("/")
async def delete_all_events(session = Depends(get_session)) -> dict:
    events = session.exec(select(Event)).all() # 전체 이벤트 불러오기 
    for event in events:
        session.delete(event)
    session.commit()
    
    return{
        "Message":"Evnets deleted successfully."
    }

# 특정 ID 업데이트 라우터 
@event_router.put("/edit/{id}")
async def update_event(id: int, new_data: EventUpdate, session = Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        # model_dump는 Pydantic v2에서 모델 데이터를 dict 형태로 변환 
        # exclude_unset = True는 사용자가 명시적으로 입력하지 않은 필드는 제외(전달된 필드만 업데이트용으로 받음)
        event_data = new_data.model_dump(exclude_unset = True) 
        for key, value in event_data.items():
            setattr(event, key, value) # 객체 event의 속성 key의 값을 value로 동적 할당 
            
        session.add(event)
        session.commit()
        session.refresh(event)
        
        return event

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Event with supplied ID does not exist"
    )