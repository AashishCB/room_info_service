from typing import Annotated
from fastapi import Depends, FastAPI, Form, UploadFile, status

from sqlalchemy.orm import Session

from room_info import crud, models

from room_info.tags import Tags
from room_info.database import SessionLocal, engine
from room_info.schemas.single_room_info_schema import SingleRoomInfoSchema
from room_info.schemas.room_schemas import RoomSchema
from room_info.schemas.room_type_schemas import RoomTypeResponseSchema, RoomTypeSchema, RoomTypeBaseSchema

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# a = s3.upload_file(
#     Filename="correlation-accident_serverity.png",
#     Bucket="cbs3bucketdottwo",
#     Key="folder/file4",
# )
# print(a)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/room_types", response_model=RoomTypeResponseSchema, status_code=status.HTTP_201_CREATED, tags=[Tags.ROOM_TYPE])
def create_room_type(room_type: RoomTypeBaseSchema, db: Session = Depends(get_db)):
    """
        Create a room type with all the information:

        - **name**: each room type must have a name
        - **description**: a long description
        - **price**: required
    """
    crud.get_room_type_by_name_or_400(db, name=room_type.name)
    return crud.create_room_type(db=db, room_type=room_type)


@app.get("/room_types", response_model=list[RoomTypeSchema], tags=[Tags.ROOM_TYPE])
def read_room_types(limit: int = 100, db: Session = Depends(get_db)):
    """
        Get room types with all the information and rooms information
    """
    room_type = crud.get_room_types(db, limit=limit)
    return room_type


@app.post("/room_types/{room_type_id}/rooms", response_model=RoomSchema, status_code=status.HTTP_201_CREATED, tags=[Tags.ROOM])
def create_room(room_type_id: int, db: Session = Depends(get_db)):
    """
        Create a room for a room type:

        - **room_type_id**: each room must have a room_type_id
    """
    crud.get_room_type_by_id_or_404(db, room_type_id=room_type_id)
    return crud.create_room(db=db, room_type_id=room_type_id)


@app.get("/room_types/{room_type_id}/rooms", response_model=list[RoomSchema], tags=[Tags.ROOM])
def read_rooms(room_type_id: int, occupancy: bool = None, limit: int = 100, db: Session = Depends(get_db)):
    """
        Get rooms for a room type

        - **room_type_id**: id of the room type
    """
    crud.get_room_type_by_id_or_404(db, room_type_id=room_type_id)
    rooms = crud.get_rooms_by_room_type(db, room_type_id=room_type_id, limit=limit, occupancy=occupancy)
    return rooms


@app.get("/rooms/{room_id}", response_model=SingleRoomInfoSchema, tags=[Tags.ROOM])
def read_room(room_id: int, db: Session = Depends(get_db)):
    """
        Get room information

        - **room_id**: id of the room
    """
    db_room = crud.get_room_by_id_or_404(db, room_id=room_id)
    return db_room


@app.put("/rooms/{room_id}", response_model=RoomSchema, tags=[Tags.ROOM])
def update_room_occupancy(room_id: int, occupied_by: str, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id_or_404(db, room_id=room_id)
    return crud.update_room_occupancy(db=db, db_room=db_room, occupied_by=occupied_by)


@app.get("/rooms/customers/{customer_id}", response_model=SingleRoomInfoSchema)
def get_customer_room(customer_id: str, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_customer_id_or_404(db=db, customer_id=customer_id)
    return db_room


@app.post("/image")
def upload_image(image: UploadFile, resource_name: Annotated[str, Form()]):
    print(image)
    return {'type': resource_name}
