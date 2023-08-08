from typing import Annotated
from fastapi import FastAPI, Form, UploadFile

from room_info import models
from room_info.aws.s3.s3_resource import s3_client
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


@app.post("/image")
def upload_image(image: UploadFile, resource_name: Annotated[str, Form()]):
    print(image)

    # s3_client.upload_file(
    #     # Filename="filename",
    #     Bucket="bucket_name",
    #     Key="upload_location")

    return {'type': resource_name}
