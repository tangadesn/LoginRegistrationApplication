from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Employee

import random
import requests
from django.core.mail import send_mail
from django.conf import settings


def indexView(request):
    return render(request, 'index.html')

def loginView(request):
    return render(request, 'authentication/login.html')

def logoutView(request):
    request.session.flush()
    return redirect('/login/')

def verifyView(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if username and password:
        emp = Employee.objects.filter(email_id=username, password=password)
        if emp:
            request.session["user_name"] = emp[0].email_id

            # otp = settings.OTP
            recepient = emp[0].email_id
            otp_device = request.POST.get("otp_device")
            if otp_device == "mobile_device":
                receiver = emp[0].mobile_number
                status, user_otp = send_sms(receiver)
            else:
                status, user_otp = send_email(recepient)
            request.session["user_otp"] = user_otp
            return render(request, 'authentication/verify_user.html')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')

def generate_otp():
    """generate random nubmer of 6 digits
    """
    return random.randint(100000, 999999)

def send_sms(receiver):
    """ send_sms will send otp through mobile 
    """
    user_otp = generate_otp()
    message = 'Here is your otp to login to\
        Employee Management System. OTP : {}'.format(user_otp)
    #change sender_id, user_type with your value
    status = sendGetRequest(settings.SMS_URL, settings.SMS_API_KEY,
                            settings.SMS_SECRET_KEY, "user_type", receiver, "sender_id", message)
    return status, user_otp

def send_email(recepient):
    """
    """
    # send email with otp
    user_otp = generate_otp()
    subject = 'Welcome to Jumanji'
    message = 'Here is your otp to login to\
        Employee Management System. OTP : {}'.format(user_otp)
    status = send_mail(subject, message, settings.EMAIL_HOST_USER,
            [recepient], fail_silently=False)
    return status, user_otp

def dashboardView(request):
    user = request.session.get("user_name", None)
    print("in dashboard ",user)
    if user:
        user_otp = request.POST['otp']
        validation_user_otp = request.session.get("user_otp")
        print("user_otp : ", user_otp)
        print("validation_user_otp : ", validation_user_otp)
        if int(user_otp) == validation_user_otp:
            del request.session["user_otp"]
            return render(request, 'dashboard.html')
        else:
            request.session.flush()
            return redirect('/login')
    else:
        request.session.flush()
        return redirect('/login/')


def registerView(request):

    return render(request, 'authentication/register.html')


def userregistrationView(request):

    if request.method == 'POST':
        email_id = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = int(request.POST['mobile'])

        e = Employee()

        e.email_id = email_id
        e.name = name
        e.password = password
        e.mobile_number = mobile
        e.save()

        return redirect('/login')

    else:
        return redirect('')

def sendGetRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
    req_params = {
        'apikey': apiKey,
        'secret': secretKey,
        'usetype': useType,
        'phone': phoneNo,
        'message': textMessage,
        'senderid': senderId
    }
    return requests.get(reqUrl, req_params)
