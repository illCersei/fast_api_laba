import time
import uuid
import json
from app.celery.worker_app import app
from app.services import binary
from redislite import Redis

@app.task(bind=True)
def binarize_image_task(self, image_base64: str, user_id: str, algorithm: str = "bradley"):
    redis = Redis("/tmp/celerydb.rdb")
    task_id = self.request.id or str(uuid.uuid4())

    def publish(msg):
        redis.publish(f"user:{user_id}", json.dumps(msg))

    self.update_state(state="STARTED")
    publish({
        "status": "STARTED",
        "task_id": task_id,
        "algorithm": algorithm
    })

    for progress in range(0, 100, 25):
        time.sleep(0.3)
        publish({
            "status": "PROGRESS",
            "task_id": task_id,
            "progress": progress
        })

    image_np = binary.decode_base64_to_image(image_base64)
    binarized_np = binary.bradley_threshold(image_np)
    result_base64 = binary.encode_image_to_base64(binarized_np)

    publish({
        "status": "COMPLETED",
        "task_id": task_id,
        "binarized_image": result_base64
    })

    return result_base64
