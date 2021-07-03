from shop.recommender import Recommender
from coupons.forms import CouponApplyForm 
from django.shortcuts import render
from django.shortcuts import redirect 
from django.shortcuts import get_object_or_404 
from django.views.decorators.http import require_POST 
from shop.models import Product 
from .cart import Cart 
from .forms import CartAddproductForm 





#добавление add 
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddproductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail') 

#удаление remove
def cart_remove(request, product_id):
    cart = cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if cart:
        return redirect('cart:cart_detail')
    return redirect('/')

#подробности details 
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddproductForm(initial={'quantity': item['quantity'], 'update': True})
    coupon_apply_form = CouponApplyForm
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended_products = r.suggest_products_for(cart_products,max_results=4)
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form, 'recommended_products': recommended_products})


