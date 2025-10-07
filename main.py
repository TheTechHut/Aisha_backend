from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import re





from database import SessionLocal, Base, engine, get_db
from models import WaitingList


Base.metadata.create_all(bind=engine)


class WaitingListCreate(BaseModel):
    username: str
    phone_number: str

    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v):
        # Matches formats like: 0712345678 or +25412345678
        pattern = r'^(?:254|\+254|0)\d{9}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid Kenyan phone number format: 0712345678 or +254712345678')
        return v

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        # Only letters, spaces and hyphens, 2-50 characters
        pattern = r'^[a-zA-Z\s-]{2,50}$'
        if not re.match(pattern, v):
            raise ValueError('Username must contain only letters, spaces, or hyphens (2-50 characters)')
        return v


app = FastAPI(title="Waiting List API")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/waiting-list/", response_model=dict)
async def create_waiting_list_item(item: WaitingListCreate, db=Depends(get_db)):
    try:
        db_item = WaitingList(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return {"message": "Added to waiting list", "id": db_item.id}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Waiting List API is running"}
    


    