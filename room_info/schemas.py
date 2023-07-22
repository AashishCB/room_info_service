from pydantic import BaseModel


class RoomBase(BaseModel):
    occupied_by: str | None


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    room_id: int
    room_type_id: int

    class Config:
        orm_mode = True


class RoomTypeBase(BaseModel):
    name: str
    description: str
    price: float


class RoomTypeCreate(RoomTypeBase):
    pass


class RoomType(RoomTypeBase):
    room_type_id: int
    rooms: list[Room] = []

    class Config:
        orm_mode = True
