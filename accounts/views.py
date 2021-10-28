from django.shortcuts import render,redirect
from .models import Profile
import uuid
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login,logout
from django.conf import settings
from django.core.mail import send_mail
from .threads import *
from django.contrib import messages

# Create your views here.
def register(request):
    try :
        if request.method == "POST":
            name = request.POST['name']
          
            email = request.POST['email']
            password = request.POST['password']
    
            print(Profile.objects.filter(email=email).first())
            if Profile.objects.filter(email=email,is_verified = False).first():
                obj = Profile.objects.get(email=email,is_verified = False)
                obj.delete()

      
            elif  Profile.objects.filter(email=email,is_verified = True).first():
                messages.error(request,'Email already exists')
                return redirect('/account/register/')
 
            user = Profile.objects.create_user(username=email,email=email,name=name)
         
            user.set_password(password)
            user.save()
            thread_obj = send_verification_link(email)
            thread_obj.start()  
            return redirect('/account/token/')
        else:
            return render(request,'accounts/register.html')    



    except Exception as e:
        print(e)
    return render(request, 'accounts/register.html')


def token(request):
    return render(request,'accounts/token_send.html') 


def error_page(request):  
    return render(request,'accounts/error.html')


def  success_page(request):
    return render(request,'accounts/success.html')  

def verify(request,id):
    try:
        if not cache.get(id):
            messages.info(request, 'The link has expired')
            return redirect('/account/register/')
        user = Profile.objects.filter(email = cache.get(id)).first()
        if user:
            user.is_verified = True
            user.save()
            return redirect('/account/success/')
        else:
            return redirect('/account/error/')
    except Exception as e:
        print(e)
    return render(request,'accounts/error.html')

def login(request):
    try:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
  
            user_obj = Profile.objects.filter(username=email).first()
            print(user_obj.is_verified)
            if user_obj.is_verified == True:
                user = authenticate(username=user_obj.username, password=password)
                print(user)
                if user:
                    auth_login(request,user)
                    return redirect('/')
                else:
                    messages.info(request, 'Invalid Credentials')
                    return redirect('/account/login/')

            else:
                messages.error(request,'Your account is not verified')
                return redirect('/account/error/')
        else:
            return render(request,'accounts/login.html')
    except Exception as e:
        print(e)
    return redirect('/account/login/')    




def logout_acc(request):
    logout(request)
    return redirect('/')






def forget(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not Profile.objects.get(email=email):
                messages.info(request, 'This user does not exist. Please Signup.')
                return redirect('/account/register/')
            thread_obj = send_forgot_link(email)
            thread_obj.start()
            messages.info(request, 'We have sent you a link to reset password via mail')
            return redirect('/account/login/')
    except Exception as e:
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/forget.html")


def reset(request, token):
    try:
        if not cache.get(token):
            messages.info(request, 'The link has expired')
            return redirect('/account/login')
        else:
            customer_obj = Profile.objects.get(email = cache.get(token))
            if customer_obj:
                try:
                    if request.method == 'POST':
                        npw = request.POST.get('npw')
                        cpw = request.POST.get('cpw')
                        if npw == cpw:
                            customer_obj.set_password(cpw)
                            customer_obj.save()
                            messages.info(request, 'Password Changed successfully.')
                            return redirect('/account/login')
                except Exception as e:
                    print(e)
            else:
                messages.info(request, 'User does not exist. Please Signup')
                return redirect('/account/register/')
    except Exception as e :
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/reset.html")    