#from django.contrib.admin.views.decorators import staff_member_required 
#from django.shortcuts import get_object_or_404
#from .models import Order 
from django.urls import reverse 
from django.shortcuts import render
from django.shortcuts import redirect 
from django.shortcuts import render
from .models import OrderItem 
from .forms import OrderCreateform 
from cart.cart import Cart 
from .tasks import order_created 

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST': 
        form = OrderCreateform(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
               OrderItem.objects.create(order=order, 
                                        product=item['product'], 
                                        price=item['price'],
                                        quantity=item['quantity']
                                        )
            cart.clear()
            #асинхронная задача
            order_created.delay(order.id)
            request.session['order_id'] = order.id 
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateform() 
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


#add user views on admin panel 
#добавление пользовательских представлений в админку\
#is_active and is_staff must be True
'''
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})
    '''