# Django-Celery-RabbitMQ

# 1- what is Celery?
- it is a distributed task queue that can collect, record, schedule, and perform tasks outside of your main program.
- can send time-intensive tasks to Celery’s task queue. In that way, the web app can respond quickly to users while Celery completes expensive operations asynchronously in the background.   

**if you want to keep track of the results of your task runs, then you also need to set up a "results back-end" database.**

# 2- why use celery?
- 1- Offloading work from your app to distributed processes that can run independently of your app
    - Celery workers -> are worker processes that run tasks independently from one another and outside the context of your main service.

- 2- Scheduling task execution at a specific time, sometimes as recurring events
    - Celery beat -> is a scheduler that orchestrates when to run tasks. You can use it to schedule periodic tasks as well.

# 3- use case of celery?
**The main setup for all these different use cases will be similar.**
- Email sending
- Image processing
- Text processing
- API calls and other web requests
- Data analysis
- Machine learning model runs
- Report generation

**Celery requires a message broker (Redis, RabbitMQ, Kafka and ect) for communication, to receive tasks from the program and send results to a back-end.**

# 4- message broker or queue 
- A message broker is a software tool that facilitates services and applications to transfer messages for communication and information exchange.
- Message brokers can secure, archive, route, and dispatch messages to the appropriate recipients. 
- They operate as a bridge between various applications, allowing senders to send messages without being familiar with the location, activity, or number of recipients.

- **basic consepts:**
    - Producer: Is an endpoint which sends any kind of data, that is stored inside the message broker to distribute.
    - Consumer: Is an endpoint which asks from the message broker for data(messages).
    - Queue: Is a data type which the message broker use to store messages inside, with the logic of FIFO(First in First out).
    - Exchange: A logical configuration or even entity, on top of the queues, which tells the message broker to create some sort of a group, which a consumers/producers can write or listen to, to send/receive messages.

- **There are two basic forms of communications with a message broker:**
   - Point-to-point messaging: 
    - the sender and recipient of each message are associated on a one-to-one basis. 
    - Every message in the queue is read only once and only sent to one recipient.
    - If the consumer is offline, the message broker stores it in the message queue and delivers it at a later time.

   - Publish/subscribe messaging: 
    - the producer is completely unaware of who will be the consumer of the message.
    - It sends messages concerning a topic, and all applications that have subscribed to it receive all published messages. 
    - The consumer and producer have a one-to-many relationship.

- **life cycle of a message broker:**
    - The cycle starts with sending messages to single or several destinations.
    - Then convert messages to a different model.
    - Split messages into smaller parts, transmit them to the consumer, and then collects the answers and convert them into a single message to send back to the user.
    - Use third-party storage to add to or store a message.
    - Fetch the required data using the web services
    - Send responses in case of message failure or errors.
    - Use the publish-subscribe pattern to route messages based on content and topic.

# 5- how add it in the project?

- **1- make a django app:**
    - python -m venv venv
    - source venv/bin/activate
    - python -m pip install django
    - django-admin startproject core .
    - python manage.py startapp app
    - python manage.py makemigrations
    - python manage.py migrate
    - python manage.py runserver

- **2- install celery and rabbitmq:**
    - python -m pip install celery
    - sudo apt install rabbitmq-server
    - sudo systemctl enable rabbitmq-server
    - sudo systemctl start rabbitmq-server
    - systemctl status rabbitmq-server

- **3- add celery in django project :**
    - 1- create celery.py file in django project and add these: 
        - import os
        - from celery import Celery
        - os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
        - app = Celery('project_name')
        - app.config_from_object('django.conf:settings',namespace='CELERY')
        - app.autodiscover_tasks()
        - @app.task(bind=True)
        - def debug_task(self):
            - print(f'Request: {self.request!r}')

    - 2- import this app in your proj/proj/__init__.py module:
        - from .celery import app as celery_app
        - __all__ = ('celery_app',)

    - 3- add Celery Configuration Options in settings.py for example:
        - CELERY_TIMEZONE = "Australia/Tasmania"
        - CELERY_TASK_TRACK_STARTED = True
        - CELERY_TASK_TIME_LIMIT = 30 * 60
        - ...

- **4- add tasks.py inside each app of django project:**
    - the @shared_task decorator lets you create tasks without having any concrete app instance
    - inside tasks.py add:
        - from app.models import myModel
        - from celery import shared_task

        - @shared_task
        - def fun_name(sth):
            - do sth on myModel
            - return sth

        - ect tasks ...

- **5- run and test the task:**
    - open 2 terminals 
    - at the first one:
        - celery -A core worker -l info
    - at the second:
        - python manage.py shell
        - from app.tasks import add
        - add.delay(4,1) or add.apply_async((3,3), countdown=5)
        - now at the first terminal you can see the result.

# 6- what's going on in the project?
- 1- simple task for understanding celery mechanism.

- 2- send feedback email. 
    - explain the steps as comments

- 3- scheduling with celery-beat
    - pip install django-celery-beat
    - add the django_celery_beat module to INSTALLED_APPS in your Django project’ settings.py 
    - apply Django database migrations so that the necessary tables are created:
        - python manage.py migrate
    - add this in settings.py
        - CELERY_BEAT_SCHEDULE = {
            - "scheduled_task": {
                - "task": "app.tasks.add",
                - "schedule": 5.0,
                - "args": (14, 15),
            - },
        - }
        - you can also make super user and define it in admin panel.
    - start the celery beat service
        - if add the task in settings -> celery -A core beat -l INFO
        - if add it from admin panel -> celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

- 4- monitoring tasks with flower:
    - pip install flower
    - celery flower --port==5566
    - in the browser enter '127.0.0.1:5566'

- 5- store celery result 
    - pip install django-celery-results
    - add the django_celery_results module to INSTALLED_APPS and
    also CELERY_RESULT_BACKEND = 'django-db'
    in your Django project’ settings.py 
    - apply Django database migrations so that the necessary tables are created:
        - python manage.py migrate django_celery_results


# sources:
- **https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-celery-with-django**
- **https://realpython.com/asynchronous-tasks-with-django-and-celery/**
- **https://geekflare.com/top-message-brokers/**
- **https://docs.djangoproject.com/en/4.1/topics/email/**
- **https://flower.readthedocs.io/en/latest/install.html**
- **https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#introduction**