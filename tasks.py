import random
import time

from celery import Celery, Task
from celery.signals import after_task_publish
from tqdm import trange

from logger import logger


Celery_app = Celery(
    __name__,
    broker_connection_retry_on_startup=True,
    broker='redis://host.docker.internal:6379/0',
    backend='redis://host.docker.internal:6379/0'
)
# Celery_app = Celery(
#     __name__,
#     broker_connection_retry_on_startup=True,
#     broker='redis://localhost:6379/0',
#     backend='redis://localhost:6379/0'
# )

class CRW4Automation(Task):
    def run(self, x, y):
        for current in range(x, 100, y):
            self.update_state(state='PROGRESS', meta={'current': current})
            print(current)
            time.sleep(2)
        return {'status': 'complete'}


CRW4Auto = Celery_app.register_task(CRW4Automation())

@Celery_app.task()
def process_data(data_id):
    logger.info(f"Processing data with ID: {data_id}")
    for i in trange(0, 100, 10):
        time.sleep(1)

    logger.info(f"Data {data_id} processed")
    return f"Data {data_id} processed"

@Celery_app.task(bind=True)
def count(self):
    for i in range(20):
        self.update_state(status='PROGRESS', meta={'current': i, 'total': 20})
        time.sleep(1)
    return {'status': 'complete'}


#Celery_register = Celery_app.register_task(MyCelery())

# Register a task in the task registry.
# The task will be automatically instantiated if not already an instance. Name must be configured prior to registration.
