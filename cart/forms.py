from django import forms 

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)] 

class CartAddproductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)#units of product количесвто единиц товара
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)#add in cart product 