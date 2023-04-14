# 6- create tasks.py and define the task for celery.
from celery import shared_task
from celery.utils.log import get_task_logger
from .email import send_suggestion_email

logger = get_task_logger(__name__)

# the task name
@shared_task(name="send_suggestion_email_task")
def send_suggestion_email_task(name, email, suggestion):
    logger.info("sent suggestion.") # a message in output.
    return send_suggestion_email(name, email, suggestion) # run the task.