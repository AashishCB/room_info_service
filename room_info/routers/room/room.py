from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from room_info import crud
from room_info.dependencies import get_db
from room_info.schemas.room_schemas import RoomSchema
from room_info.schemas.single_room_info_schema import SingleRoomInfoSchema
from room_info.tag import Tag

router = APIRouter(
    prefix="/rooms",
    tags=[Tag.ROOM],
    dependencies=[Depends(get_db)]
)


@router.get("/{room_id}", response_model=SingleRoomInfoSchema)
def read_room(room_id: int, db: Session = Depends(get_db)):
    """
        Get room information

        - **room_id**: id of the room
    """
    db_room = crud.get_room_by_id_or_404(db, room_id=room_id)
    return db_room


@router.put("/{room_id}", response_model=RoomSchema)
def update_room_occupancy(room_id: int, occupied_by: str, db: Session = Depends(get_db)):
    """
        Check-In/Check-Out customer from room

        - **room_id**: id of the room
    """
    db_room = crud.get_room_by_id_or_404(db, room_id=room_id)
    return crud.update_room_occupancy(db=db, db_room=db_room, occupied_by=occupied_by)


@router.get("/customers/{customer_id}", response_model=SingleRoomInfoSchema)
def get_customer_room(customer_id: str, db: Session = Depends(get_db)):
    """
        Find room of the customer

        - **customer_id**: id of the customer checked-in
    """
    db_room = crud.get_room_by_customer_id_or_404(db=db, customer_id=customer_id)
    return db_room
