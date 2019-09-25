from celery import Celery
import os

def make_celery(app):

    if os.environ.get('FLASK_ENV') == 'development':
        celery = Celery(
            app.import_name,
            backend=os.environ.get('CELERY_RESULT_BACKEND'),
            broker=os.environ.get('CELERY_BROKER_URL')
        )
    elif os.environ.get('FLASK_ENV') == 'production':
        celery = Celery(
            app.import_name,
            backend=os.environ.get('CLOUDAMQP_URL'),
            broker=os.environ.get('CLOUDAMQP_URL')
        )
    
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery