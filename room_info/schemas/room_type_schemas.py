from pydantic import BaseModel

from room_info.schemas.room_schemas import RoomListSchema


class RoomTypeBaseSchema(BaseModel):
    name: str
    description: str
    price: float


class RoomTypeResponseSchema(RoomTypeBaseSchema):
    room_type_id: int


class RoomTypeSchema(RoomTypeBaseSchema):
    room_type_id: int
    rooms: list[RoomListSchema]

    class Config:
        from_attributes = True
