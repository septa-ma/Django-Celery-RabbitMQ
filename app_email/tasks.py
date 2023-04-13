from celery.decorators import task
from celery.utils.log import get_task_logger
from .email import send_suggestion_email

logger = get_task_logger(__name__)

@task(name="send_suggestion_email_task")
def send_suggestion_email_task(name, email, suggestion):
    logger.info("sent suggestion.")
    return send_suggestion_email(name, email, suggestion)