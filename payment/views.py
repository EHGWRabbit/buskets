import braintree
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404 
from orders.models import Order 


#function payment 
def payment_process(request):
    order_id = request.session.get('order_id')#получаем заказ
    order = get_object_or_404(Order, id=order_id)#извлекаем обьект Order или ошибку если его нет
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)#создаем новую транзакцию
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),#общая сумма
            'payment_method_nonce': nonce,#токен оплаты
            'options': {
                'submit_for_settlement': True#представление транзакции к расчету
            }
        })
        if result.is_success:
            order.paid = True#если успешно обработана транзакция ставим истину
            order.braintree_id = result.transaction.id#сохраняем идентификатор шлюза
            order.save()
            return redirect('payment:done')#еренаправление на завершение
        else:
            return redirect('payment:canceled')#перенаправление на повтор
    else:
         client_token = braintree.ClientToken.generate()
         return render(request, 
                      'payment/process.html', 
                      {'order': order,
                       'client_token': client_token})


#представление для успешного оформления
def payment_done(request):
    return render(request, 'payment/done.html')

#представление для не удачного оформления
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
