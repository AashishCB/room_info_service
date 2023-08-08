from room_info.schemas.room_schemas import RoomListSchema
from room_info.schemas.room_type_schemas import RoomTypeResponseSchema


class SingleRoomInfoSchema(RoomListSchema):
    room_type: RoomTypeResponseSchema

    class Config:
        from_attributes = True
