from django.db import models
from django.core.validators import MinValueValidator 
from django.core.validators import MaxValueValidator 

#model coupon 
class Coupon(models.Model):
    #cod into to site for user bay
    #код, необходимый для скидки
    code = models.CharField(max_length=50, unique=True, verbose_name='Код купона')
    #valid time begin move coupons 
    #время начала дейстия купона
    valid_from = models.DateTimeField()
    #time end move coupon 
    #мя окончания действия купона
    valid_to = models.DateTimeField()
    #скидка
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    #activ coupon or no
    #активен ли купон 
    active = models.BooleanField()


    def __str__(self):
        return self.code
