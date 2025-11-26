FROM python:3.11-slim
WORKDIR /worker

# copy requirements from project root/backend/
COPY backend/requirements.txt /worker/requirements.txt
RUN pip install --no-cache-dir -r /worker/requirements.txt

# copy app from project root/backend/app
COPY backend/app /worker/backend/app

# optional: remove req file to keep image tidy
RUN rm -f /worker/requirements.txt

CMD ["celery", "-A", "backend.app.tasks.celery", "worker", "--loglevel=info", "--concurrency=2"]
