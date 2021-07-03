'''from django import forms 
from django.contrib.auth.models import User 
from .models import Profile 


#форма аутентификации
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#форма регистрации нового пользователя
#form for registration new user 
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пжлст', widget=forms.PasswordInput)

    class Meta:
        model = User 
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):#щчищаем поле ввода подтверждающего пароль clean up 
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']



#форма для редактирвания своего профиля
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ('date_of_birth', 'photo')
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
'''