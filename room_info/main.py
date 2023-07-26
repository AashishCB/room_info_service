from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/room_types/", response_model=schemas.RoomType)
def create_room_type(room_type: schemas.RoomTypeCreate, db: Session = Depends(get_db)):
    crud.get_room_type_by_name_or_400(db, name=room_type.name)
    return crud.create_room_type(db=db, room_type=room_type)


@app.get("/room_types/", response_model=list[schemas.RoomType])
def read_room_type(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    room_type = crud.get_room_types(db, skip=skip, limit=limit)
    return room_type


@app.post("/room_types/{room_type_id}/rooms/", response_model=schemas.Room)
def create_room(room_type_id: int, db: Session = Depends(get_db)):
    crud.get_room_type_by_id_or_400(db, room_type_id=room_type_id)
    return crud.create_room(db=db, room_type_id=room_type_id)


@app.get("/room_types/{room_type_id}/rooms/", response_model=list[schemas.Room])
def read_rooms(room_type_id: int, occupancy: bool = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_rooms_by_room_type(db, room_type_id=room_type_id, skip=skip, limit=limit, occupancy=occupancy)
    return rooms


@app.get("/rooms/{room_id}/", response_model=schemas.Room)
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id_or_400(db, room_id=room_id)
    return db_room


@app.put("/rooms/{room_id}/", response_model=schemas.Room)
def update_room_occupancy(room_id: int, occupied_by: str, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id_or_400(db, room_id=room_id)
    return crud.update_room_occupancy(db=db, db_room=db_room, occupied_by=occupied_by)


@app.get("/rooms/customers/{customer_id}", response_model=schemas.Room)
def get_customer_room(customer_id: str, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_customer_id_or_400(db=db, customer_id=customer_id)
    return db_room
