'''
Этот файл создан для размещения задач для их выполнения
aсинхронно с помощью celery
'''
import celery
from celery import task
from django.core.mail import send_mail 
from .models import Order 

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Заказ nr. {}'.format(order.id) 
    message = 'Уважаемый {}, \n\nВы успешно заполнили бланк заказа. Номер вашего заказа {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, 'admin@my-flowers-eat-shop.herokuapp.com', [order.email])

    return mail_sent