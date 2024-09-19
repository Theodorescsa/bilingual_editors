from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE",'django_celery_project.settings')
app = Celery('django_celery_project')
app.conf.enable_utc = False

app.conf.update(timezone = "Asia/Kolkata")
app.config_from_object(settings,namespace='CELERY')

app.conf.beat_chedule = {}
app.autodiscover_tasks()

app.conf.task_queues = {
    'add':{
        'exchange': 'add',
        'exchange_type': 'direct',
        'binding_key': 'add',
    },

    'download_queue': {
        'exchange': 'download',
        'exchange_type': 'direct',
        'binding_key': 'download',
    },
    'audio_queue': {
        'exchange': 'audio',
        'exchange_type': 'direct',
        'binding_key': 'audio',
    },
    'transcribe_queue': {
        'exchange': 'transcribe',
        'exchange_type': 'direct',
        'binding_key': 'transcribe',
    },
    'generate_subtitle_queue': {
        'exchange': 'generate_subtitle',
        'exchange_type': 'direct',
        'binding_key': 'generate_subtitle',
    },
    'add_subtitle_queue': {
        'exchange': 'add_subtitle',
        'exchange_type': 'direct',
        'binding_key': 'add_subtitle',
    },
}

app.conf.task_routes = {
    'tasks.add':{'queue':'add_queue'},
    'tasks.download_video': {'queue': 'download_queue'},
    'tasks.extract_audio': {'queue': 'audio_queue'},
    'tasks.transcribe': {'queue': 'transcribe_queue'},
    'tasks.generate_subtitle_file': {'queue': 'generate_subtitle_queue'},
    'tasks.add_subtitle_to_video': {'queue': 'add_subtitle_queue'},
}

app.conf.worker_pool = 'threads'
app.conf.worker_concurrency = 4
app.conf.broker_connection_retry_on_startup = True

import tasks

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
    
    