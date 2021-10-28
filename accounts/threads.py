import threading, random, uuid
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
from decouple import config

Web_address = config('WEB_ADDRESS')

class send_verification_link(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        try:
            token = str(uuid.uuid4())
            cache.set(token, self.email, timeout=350)
            subject = "Link to verify the your Account"
            message = f"The link to verify your account  {Web_address}account/verify/{token} \nIts valid only for 5 mins."
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
         
            send_mail(subject , message ,email_from ,[self.email], fail_silently=False)
            print("Email send finished")
        except Exception as e:
            print(e)

class send_forgot_link(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        try:
            token = str(uuid.uuid4())
            cache.set(token, self.email, timeout=350)
            subject = "Link to change password"
            message = f"The link to change your account password {Web_address}account/reset/{token} \nIts valid only for 5 mins."
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
                print(e)