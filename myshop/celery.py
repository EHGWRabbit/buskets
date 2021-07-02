import os 
from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')#set variable for celerycli 

app=Celery('myshop')#create app with celery 

app.config_from_object('django.conf:settings', namespace='CELERY')#configuration from project 
app.autodiscover_tasks()#start search asinhronic tasks