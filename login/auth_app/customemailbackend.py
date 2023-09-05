from django.shortcuts import render,HttpResponse,redirect
from django. contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            # Check if the email address matches the custom domains
            user = UserModel.objects.get(email=email, is_active=True)
            if user.is_staff is False:
                if email.endswith(('pg.ictmumbai.edu.in', 'ug.ictmumbai.edu.in')):
                    if user.check_password(password):
                        return user
                else:
                    messages.error(request, 'Email must use pg.ictmumbai.edu.in or ug.ictmumbai.edu.in domain')
                    return None
            elif user.is_superuser:
                if email.endswith(('pg.ictmumbai.edu.in', 'ug.ictmumbai.edu.in')):
                        if user.check_password(password):
                            return user
                else:
                    messages.error(request, 'Superusers must use pg.ictmumbai.edu.in domain')
                    return None

        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
