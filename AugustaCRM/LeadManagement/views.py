# Create your views here.
from django.shortcuts import render , redirect
from django.http import HttpResponse
import pyrebase
from django.contrib import auth

import os

FIREBASE_CONFIG = {
    'apiKey': str(os.getenv('FIREBASE_API_KEY')),
    'authDomain': str(os.getenv('FIREBASE_AUTH_DOMAIN')),
    'databaseURL': str(os.getenv('FIREBASE_DATABASE_URL')),
    'projectId': str(os.getenv('FIREBASE_PROJECT_ID')),
    'storageBucket': str(os.getenv('FIREBASE_STORAGE_BUCKET')),
    'messagingSenderId': str(os.getenv('FIREBASE_MESSAGING_SENDER_ID')),
    'appId': str(os.getenv('FIREBASE_APP_ID')),
    'measurementId': str(os.getenv('FIREBASE_MEASUREMENT_ID')),
}

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth_fb = firebase.auth()

def index(request):
    return render(request, "index.html",{"next_action":"services/"})

def services(request):
    email=request.POST.get('email')
    password=request.POST.get('password')  
    try: 
        user=auth_fb.sign_in_with_email_and_password(email, password)
        print(user)
        return render(request, "services.html")
    except:
        return render(request, "index.html", {"messages":"Invalid Credentials try again"})

def sign_up(request):
    return render(request, "sign_up.html")

def logout(request):
    auth.logout(request)
    return render(request, "index.html")

def CallLeads(request):
    return render(request, "call-leads.html")

def calendly(request):
    return render(request, "calendly.html")

def ResultLog(request):
    return render(request, "result-log.html")

def CallBackLater(request):
    # Crud operation code
    return redirect('/services/call-leads/result-log')

def NotAnswered(request):
    #Crud operation code
    return redirect('/services/call-leads/result-log')

def NotIntrested(request):
    #Crud operation code
    return redirect('/services/call-leads/result-log')