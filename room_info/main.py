from typing import Annotated
from fastapi import FastAPI, Form, UploadFile

from room_info import models
from room_info.routers.room_type import room_type
from room_info.routers.room import room
from room_info.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(room_type.router)
app.include_router(room.router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

# a = s3.upload_file(
#     Filename="correlation-accident_serverity.png",
#     Bucket="cbs3bucketdottwo",
#     Key="folder/file4",
# )
# print(a)


@app.post("/image")
def upload_image(image: UploadFile, resource_name: Annotated[str, Form()]):
    print(image)
    return {'type': resource_name}
