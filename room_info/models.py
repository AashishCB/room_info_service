from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from room_info.database import Base


class RoomType(Base):
	__tablename__ = "room_types"
	
	room_type_id = Column(Integer, primary_key=True)
	name = Column(String, unique=True, index=True)
	description = Column(String)
	price = Column(Float)

	rooms = relationship("Room", back_populates="room_type")


class Room(Base):
	__tablename__ = "rooms"

	room_id = Column(Integer, primary_key=True)
	occupied_by = Column(String)
	room_type_id = Column(Integer, ForeignKey("room_types.room_type_id"))

	room_type = relationship("RoomType", back_populates="rooms")
