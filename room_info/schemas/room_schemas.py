from pydantic import BaseModel


class RoomBaseSchema(BaseModel):
    occupied_by: str | None


class RoomListSchema(RoomBaseSchema):
    room_id: int


class RoomSchema(RoomListSchema):
    room_type_id: int
