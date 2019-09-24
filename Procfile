web: python migrate.py; gunicorn start:app --preload
celery: celery -A app.celery worker --loglevel=info