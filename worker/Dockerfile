FROM python:3.11-slim
WORKDIR /worker
COPY ../backend/app /worker/backend/app
RUN pip install --no-cache-dir -r /worker/backend/app/../requirements.txt
CMD ["celery", "-A", "backend.app.tasks.celery", "worker", "--loglevel=info", "--concurrency=2"]
