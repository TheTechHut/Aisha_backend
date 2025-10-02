from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import SessionLocal, Base, engine, get_db
from models import WaitingList


Base.metadata.create_all(bind=engine)


class WaitingListCreate(BaseModel):
    username: str
    phone_number: str


app = FastAPI(title="Waiting List API")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/waiting-list/", response_model=dict)
def create_waiting_list_item(item: WaitingListCreate, db=Depends(get_db)):
    db_item = WaitingList(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Added to waiting list", "id": db_item.id}

@app.get("/")
def read_root():
    return {"message": "Waiting List API is running"}
