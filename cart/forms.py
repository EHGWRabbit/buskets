from django import forms 
from django.utils.translation import gettext_lazy as _ 

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)] 

class CartAddproductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Количество')#units of product количесвто единиц товара
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)#add in cart product 