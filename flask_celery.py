from celery import Celery
import os

def make_celery(app):
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