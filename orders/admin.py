#from django.urls import reverse 
#from django.utils.safestring import mark_safe
import csv 
import datetime 
from django.http import HttpResponse 
from django.contrib import admin
from .models import Order, OrderItem 


#function export to csv from order 
#ункция ппреобразования заказа в формат csv 
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta 
    response = HttpResponse(content_type='text/csv')#создаем экземляр httpresponcse / create httpresponse exsemple
    #тем самым сообщаем браузеру, что нам нужен csv
    response['Content-Disposition'] = 'attachment;','filename={}.csv'.format(opts.verbose_name)#показываем, что
    #ответ содержит приклепленный файл
    #show what response with csv file

    #create place to write csv
    writer = csv.writer(response)#создаем место куда запишем csv
    #get fields and exect options many_to_many an one_to_many
    #получаем поля модели и исключаем отношения
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    #write string set and include names of fields
    #пишем строку зашголовка и имена полей
    writer.writerow([field.verbose_name for field in fields])
    #with for queryset and write string for every object
    #перебираем queryset и записываем строку для каждого объекта
    #выходное знгачение обязано быть в формате строки
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response 
#show name 
export_to_csv.short_description = 'Export to csv'


class OrderIteminline(admin.TabularInline):
    model = OrderItem 
    raw_id_fields = ['product']

#функция принимает в качестве аргумента Order 
#возвращает сссылку 
#this function get as argument Order 
#return html a and delete enter
#acros xss escape user intered! with dfunction mark_safe
'''
def order_detail(obj):
    return mark_safe('<a href="{}">Показать</a>'.format(reverse('orders:admin_order_detail', args=[obj.id])))
'''
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']#, order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderIteminline]
    actions = [export_to_csv]

