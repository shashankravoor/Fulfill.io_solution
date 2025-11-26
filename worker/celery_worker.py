from celery import Celery
from backend.app.config import settings
from backend.app.tasks import celery as tasks_celery

# Create worker app -- uses same celery app defined in tasks.py
app = tasks_celery

if __name__ == "__main__":
    app.worker_main()
