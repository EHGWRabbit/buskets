import redis 
from django.conf import settings 
from .models import Product 
'''
#connecting to redis
#соединение с redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

class Recommender(object):
    def get_product_key(self, id):
        #get id for this Product
        #получаем идентификаторы для продукта
        return 'Товары :{}: приобретаются со следующими товарами'.format(id)

    def product_bought(self, products):
        #recurs loop id products acros one is one product 
        #перебираем идентификаторы продуктов
        #перебираем для каждого идетификатора перебираем все идентификаторы
        #чтобы найти взаимосвязь
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    #get key product redis
                    #and +1 rasiting product
                    #увеличиваем рейтинг продкта основываясь на данных 
                    #о его покупках
                    r.zincrby(self.get_product_key(product_id), with_id, amount=1)

    #method getting products wich bay togever
    #функция извлечения продуктов, покупаемых вместе

    def suggest_products_for(self, products, max_results=6):
        #list product for recommendations 
        #список продуктьов для рекомендаций
        #max-results - max recomandations
        #максимальное число рекомендаций
        #получаем идентификаторы продуктов
        product_ids = [p.id for p in products]
        #если один то получаем идентификаторы продуктов купленных с ним
        if len(products) == 1:
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            #if more one product create key redis
            #когда более одного продукта, поручаем редис создать ключь
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            keys = [self.get_product_key(id) for id in product_ids]
            #unit sorted set keys 
            #обьединяем созданные временые ключи 
            r.zunionstore(tmp_key, keys)
            #emove products
            #удачяем из набора продукты, оставив только баллы
            r.zrem(tmp_key, *product_ids)
            #out from id 
            #извлекаем идентификаторы из временного ключа ограничиваемся 
            #максимальным результатом заданным ранее
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            #remove key
            #удаляем ключ
            r.delete(tmp_key)
            #get products and sorted it 
            #получаем продукты и сортеруем их
        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    #clear recommendations
    #чистка рекомендаций
    def clear_purchses(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))

'''