celery: celery -A app.celery worker --loglevel=info
web: python migrate.py; gunicorn start:app --preload