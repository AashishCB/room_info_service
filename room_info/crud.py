from fastapi import HTTPException

from sqlalchemy.orm import Session

from room_info import models
from room_info.schemas.room_type_schemas import RoomTypeBaseSchema


def get_room_types(db: Session, limit: int = 100):
    return db.query(models.RoomType).limit(limit).all()


def create_room_type(db: Session, room_type: RoomTypeBaseSchema):
    db_room_type = models.RoomType(name=room_type.name, description=room_type.description, price=room_type.price)
    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    return db_room_type


def update_availability_for_room_type(db: Session, db_room_type, reserve):
    if reserve:
        db_room_type.available = db_room_type.available - 1
    else:
        db_room_type.available = db_room_type.available + 1

    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    return db_room_type


def get_room_type_by_name_or_400(db, name: str):
    db_room_type = db.query(models.RoomType).filter(models.RoomType.name == name).first()
    if db_room_type:
        raise HTTPException(status_code=400, detail="Room type already exists")
    return db_room_type


def get_room_type_by_id_or_404(db, room_type_id: int):
    db_room_type = get_room_type_by_id(db, room_type_id)
    if not db_room_type:
        raise HTTPException(status_code=404, detail=f"Room Type {room_type_id} not found")
    return db_room_type


def get_room_type_by_id(db, room_type_id):
    return db.query(models.RoomType).filter(models.RoomType.room_type_id == room_type_id).first()


def create_room(db: Session, room_type_id: int):
    db_room = models.Room(room_type_id=room_type_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def get_rooms_by_room_type(db, room_type_id: int, limit: int = 100, occupancy: bool = None):
    if occupancy is not None:
        return db.query(models.Room). \
            filter(models.Room.room_type_id == room_type_id). \
            filter(models.Room.occupied_by==None if occupancy else models.Room.occupied_by!=None). \
            limit(limit). \
            all()

    return db.query(models.Room).filter(models.Room.room_type_id == room_type_id).limit(limit).all()


def get_room_by_id_or_404(db, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail=F"Room {room_id} not found")
    return db_room


def update_room_occupancy(db: Session, db_room, occupied_by: str):
    if db_room.occupied_by == occupied_by:
        db_room.occupied_by = None
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room
    elif db_room.occupied_by is None:
        db_room.occupied_by = occupied_by
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room
    else:
        raise HTTPException(status_code=400, detail=F"Invalid customer {occupied_by} for room {db_room.room_id}")


def get_room_by_customer_id_or_404(db: Session, customer_id):
    db_room = db.query(models.Room).filter(models.Room.occupied_by == customer_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail=F"Customer {customer_id} not found")
    return db_room
