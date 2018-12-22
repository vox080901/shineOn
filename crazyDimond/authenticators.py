from .models import User
from django.core.cache import cache
from .extra import Authentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response


class LoginAuthticator(BaseAuthentication):
    def authenticate(self, request):
        account = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(account=account, password=password).first()
        if user:
            token = Authentication(account).tokenMaker()
            user.token = token
            user.save()
            request.session["account"] = account
            request.session["username"] = user.user_name
            request.session.set_expiry(60 * 60 * 24 * 7)
            cache.set(account, token)
            return (user, token)
        else:
            raise AuthenticationFailed(detail="1")

class Up2Down(BaseAuthentication):
    def authenticate(self, request):
        account = request.session.get("account")
        if not account:
            raise AuthenticationFailed(detail="1")
        else:
            username = request.session.get("username")
            user = User.objects.filter(user_name=username).first()
            cli_token = request.COOKIES.get("token")
            ser_token = cache.get(account)
            if cli_token != ser_token:
                print("*"*40)
                raise AuthenticationFailed(detail="1")
            else:
                return (user, username)

