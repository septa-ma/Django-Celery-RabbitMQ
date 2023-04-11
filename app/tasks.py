# from app.models import Post
from celery import shared_task

@shared_task
def add(x, y):
    return x + y