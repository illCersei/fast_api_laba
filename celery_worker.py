from app.celery.worker_app import app as celery_app 
import app.celery.tasks


#celery -A celery_worker.celery_app worker --loglevel=info

