from django.contrib.auth.models import User 

#создаем класс для аутентификации по адресу электронной почты
#create class for authenticate on email address 
class EmailAuthBakend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user 
            return None 
        except User.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return User.oblects.get(pk=user_id)
        except User.DoesNotExist:
            return None