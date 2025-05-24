import os
from celery import Celery
from redislite import Redis

redis_instance = Redis("/tmp/celerydb.rdb")  # файл можно указать любой

redis_socket_path = redis_instance.socket_file

redis_url = f"redis+socket://{redis_socket_path}"

app = Celery(
    "worker",
    broker=redis_url,
    backend=redis_url
)

app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
