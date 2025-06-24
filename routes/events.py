from fastapi import APIRouter, HTTPException, status, Body
from models.events import Event
from typing import List

event_router = APIRouter(
    tags = ["Events"]
)

events = []

# 모든 이벤트 추출
@event_router.get("/", response_model = List[Event]) # 출력 형식 지정 
async def retrieve_all_events() -> List[Event]:
    return events

# 특정 ID의 이벤트 추출 라우팅
@event_router.get("/{id}", response_model = Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Event with supplied ID dose not exist."
    )

# Body...?
@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    events.append(body)
    return{
        "message":"Event created successfully."
    }
    
@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return{
                "Message":"Event deleted successfully."
            }
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Event with supplied ID dose not exist"
    )
    
@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return{
        "Message":"Evnets deleted successfully."
    }