FROM python:3.11.3

WORKDIR /room_info_service_fix

COPY ./requirements.txt /room_info_service_fix/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /room_info_service_fix/requirements.txt

COPY ./room_info /room_info_service_fix/room_info

CMD ["uvicorn", "room_info.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
