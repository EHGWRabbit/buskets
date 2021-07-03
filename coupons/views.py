from django.shortcuts import render
from django.shortcuts import redirect 
from django.utils import timezone 
from django.views.decorators.http import require_POST
from .models import Coupon 
from .forms import CouponApplyForm 

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    #if form validation we are get code
    #если форма действительна, получаем код 
    if form.is_valid():
        #entered from dict
        #еденный из словаря
        code = form.cleaned_data['code']
        try:
            #try get object Coupon with code
            #предпринимаем попытку получить Купон используя код
            #use iexact for register 
            #используем iexect для полного совпадения
            #Coupon must be active now
            #купон должен быть активен
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            #save id coupon in session user
            #сохраняем идентификатор купона в сессии пользователя
            request.session['coupon_id'] = coupon.id 
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    #use coupon anfd redirec user to cart
    #применяем купон и перенаправляем пользователя на корзину
    return redirect('cart:cart_detail')
