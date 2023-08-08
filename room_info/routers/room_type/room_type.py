from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from room_info import crud
from room_info.dependencies import get_db
from room_info.schemas.room_schemas import RoomSchema
from room_info.schemas.room_type_schemas import RoomTypeSchema, RoomTypeResponseSchema, RoomTypeBaseSchema
from room_info.tag import Tag

router = APIRouter(
    prefix="/room_types",
    tags=[Tag.ROOM_TYPE],
    dependencies=[Depends(get_db)]
)


@router.post("", response_model=RoomTypeResponseSchema, status_code=status.HTTP_201_CREATED)
def create_room_type(room_type: RoomTypeBaseSchema, db: Session = Depends(get_db)):
    """
        Create a room type with all the information:

        - **name**: each room type must have a name
        - **description**: a long description
        - **price**: required
    """
    crud.get_room_type_by_name_or_400(db, name=room_type.name)
    return crud.create_room_type(db=db, room_type=room_type)


@router.get("", response_model=list[RoomTypeSchema])
def read_room_types(limit: int = 100, db: Session = Depends(get_db)):
    """
        Get room types with all the information and rooms information
    """
    room_type = crud.get_room_types(db, limit=limit)
    return room_type


@router.post("/{room_type_id}/rooms", response_model=RoomSchema, status_code=status.HTTP_201_CREATED)
def create_room(room_type_id: int, db: Session = Depends(get_db)):
    """
        Create a room for a room type:

        - **room_type_id**: each room must have a room_type_id
    """
    crud.get_room_type_by_id_or_404(db, room_type_id=room_type_id)
    return crud.create_room(db=db, room_type_id=room_type_id)


@router.get("/{room_type_id}/rooms", response_model=list[RoomSchema])
def read_rooms(room_type_id: int, occupancy: bool = None, limit: int = 100, db: Session = Depends(get_db)):
    """
        Get rooms for a room type

        - **room_type_id**: id of the room type
    """
    crud.get_room_type_by_id_or_404(db, room_type_id=room_type_id)
    rooms = crud.get_rooms_by_room_type(db, room_type_id=room_type_id, limit=limit, occupancy=occupancy)
    return rooms
