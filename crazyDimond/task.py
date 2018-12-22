import random
import redis
from celery import task
from shineOn import settings
from django.core.mail import send_mail

@task
def sendMail(email):
    auth_key = "".join(random.sample(settings.AUTH_CODE_LIST, 4))
    msg = "<h4>感谢您的注册!您的验证码是: <h3>{}</h3></h4>".format(auth_key)
    send_mail("【ShineOnCrazy.com】注册", "", settings.EMAIL_FROM, [email], html_message=msg)
    pool = redis.ConnectionPool(host='', password='',)
    r = redis.Redis(connection_pool=pool)
    r.set(email, auth_key, ex=60*5)