# Create your views here.
import json
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import auth
import pyrebase
from datetime import datetime
from .serializer import DataSerializer
from rest_framework.renderers import JSONRenderer
from .Firebase.Firedb import *



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
print(FIREBASE_CONFIG)
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth_fb = firebase.auth()
db = firebase.database()

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
    rec = newleadlist()
    
    point = rec[0]
    
    # point= db.child("local_test").child("lead_details").child("email").get()
    email = point["Email"]
    # point= db.child("local_test").child("lead_details").child("name").get()
    name =  point["Name"]
    # point= db.child("local_test").child("lead_details").child("name").get()
    phone = point["phone"]
    # point= db.child("local_test").child("lead_details").child("name").get()
    time = point["Created"]
    # point= db.child("local_test").child("lead_details").child("name").get()
    source = point["Platform"]
    return render(request, "call-leads.html", {"email": email, "name": name, "phone": phone, "time": time, "source": source})

def CallList(request):
    rec = get_Call_List()
    point = rec[0]

    email = point["Email"]
    name =  point["Name"]
    phone = point["phone"]
    time = point["Created"]
    source = point["Platform"]
    
    return render(request, "call-list.html", {"email": email, "name": name, "phone": phone, "time": time, "source": source})

def CallResult(request):
    
    return render(request, "call-result.html")

def Call(request):    
    result = db.child("Call List").get()
    result = result.val()
    rkey=""
    rec = get_Call_List()
    point = rec[0]
    attempt_no = point["Attempt_no"]
    phone = point["phone"]
    for key, value in result.items():
        rkey = key
        break
    attempt_no = attempt_no +1
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.child("Call List").child(rkey).update({"Attempt_no": attempt_no})
    db.child("Call List").child(rkey).update({"Attempted": now})
    print(phone)
    redirect(f'tel:{phone}')

    return redirect('services/call-leads/call-list/')

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