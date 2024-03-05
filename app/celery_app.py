import os
import sys
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from celery import Celery
from app.config import (CELERY_BROKER, CELERY_BACKEND, CELERY_TIMEZONE, CELERY_ACCEPT_CONTENT, CELERY_RESULT_SERIALIZER,
                        CELERY_TASK_SERIALIZER)

celery = Celery(
    "tasks",
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND,
)

celery.conf.update(
    CELERY_ACCEPT_CONTENT=CELERY_ACCEPT_CONTENT,
    CELERY_TASK_SERIALIZER=CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER=CELERY_RESULT_SERIALIZER,
    CELERY_TIMEZONE=CELERY_TIMEZONE,
)