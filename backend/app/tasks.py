from celery import Celery
from .config import settings
import csv, io, os, tempfile, logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# NOTE: For best performance we use psycopg2 COPY FROM to bulk import.
def pg_copy_from_csv(conn_info: str, csv_path: str):
    conn = psycopg2.connect(conn_info)
    try:
        with conn.cursor() as cur, open(csv_path, "r", encoding="utf-8") as f:
            # Assume CSV header matches (sku, name, description, price, available)
            cur.copy_expert("COPY products(sku, name, description, price, available) FROM STDIN WITH CSV HEADER", f)
        conn.commit()
    finally:
        conn.close()

@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def process_csv_task(self, csv_path: str):
    try:
        logger.info("Starting CSV import: %s", csv_path)
        pg_copy_from_csv(settings.DATABASE_URL, csv_path)
        # Optionally delete file after success
        try:
            os.remove(csv_path)
        except Exception:
            logger.warning("Could not delete %s", csv_path)
        return {"status": "success", "imported_file": csv_path}
    except Exception as exc:
        logger.exception("CSV import failed")
        raise self.retry(exc=exc)
