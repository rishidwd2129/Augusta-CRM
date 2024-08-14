#rishi
# Create your views here.
import json
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import auth
import pyrebase
from datetime import datetime, timedelta
from .serializer import DataSerializer
from rest_framework.renderers import JSONRenderer
from .Firebase.Firedb import *

######################################################################## custom function start #########################################################################

def hour_difference_from_now(timestamp: str) -> int:
    # Define the datetime format
    datetime_format = '%Y-%m-%d %H:%M:%S'
    
    # Convert the input timestamp to a datetime object
    dt = datetime.strptime(timestamp, datetime_format)
    
    # Get the current datetime
    now = datetime.now()
    
    # Calculate the difference in time
    time_difference = now - dt
    
    # Convert the difference to hours and return as an integer
    return int(time_difference.total_seconds() // 3600)


########################################################################  custom function end  #####################################################################

import os

''' FIREBASE_CONFIG = {
    'apiKey': str(os.getenv('FIREBASE_API_KEY')),
    'authDomain': str(os.getenv('FIREBASE_AUTH_DOMAIN')),
    'databaseURL': str(os.getenv('FIREBASE_DATABASE_URL')),
    'projectId': str(os.getenv('FIREBASE_PROJECT_ID')),
    'storageBucket': str(os.getenv('FIREBASE_STORAGE_BUCKET')),
    'messagingSenderId': str(os.getenv('FIREBASE_MESSAGING_SENDER_ID')),
    'appId': str(os.getenv('FIREBASE_APP_ID')),
    
} '''
FIREBASE_CONFIG = {
    'apiKey': 'AIzaSyAym1Kj3p0wtzkpdcrtlyE4fwaMmQ7SoIw',
    'authDomain': 'augusta-crm-system.firebaseapp.com',
    'databaseURL': 'https://augusta-crm-system-default-rtdb.firebaseio.com',
    'projectId': 'augusta-crm-system',
    'storageBucket': 'augusta-crm-system.appspot.com',
    'messagingSenderId': '267366639689',
    'appId': '1:267366639689:web:b3854a1012e58a53143798',
}
print(FIREBASE_CONFIG)
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth_fb = firebase.auth()
db = firebase.database()

rec_num=0
new_rec_num=0
def index(request):
    return render(request, "index.html",{"next_action":"services/"})

def services(request):
    global rec_num
    global new_rec_num
    rec_num=0
    new_rec_num=0
    email=request.POST.get('email')
    password=request.POST.get('password')
    try: 
        user=auth_fb.sign_in_with_email_and_password(email, password)
        session_id=user['idToken']
        request.session['uid']=str(session_id)
        return render(request, "services.html")
    except:
        return render(request, "index.html", {"messages":"Session Expired requires relogin"})

def logout(request):
    auth.logout(request)
    return render(request, "index.html")
def EmptyNewLeads(request):
    return render(request,"EmptyNewLeads.html",{"messages":"A cooldown period of 18 hours has been added to previous lead"})

def EmptyCallList(request):
    return render(request,"EmptyCall-List.html")


def CallLeads(request):
    return render(request, "call-leads.html")

def NewLeads(request):
    global new_rec_num
    try:
        rec = newleadlist()
        if not rec:
            return redirect('/empty-newleads')
           
        point = rec[new_rec_num]
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
        return render(request, "new-leads.html", {"email": email, "name": name, "phone": phone, "time": time, "source": source})
    except:
        return redirect('/empty-newleads')
def Newcalendly(request):
    new_rec_num = 0
    move_to_archive("booked")
    return render(request, "calendly.html")

def NewCallBack(request):
    global new_rec_num
    # move_to_call_list("call back later", new_rec_num)

    result = db.child("New Leads").get()
    result = result.val()
    rec = get_New_List("New Leads")
    point = rec[0]
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {"Attempted":now,"status":"call back later", "Attempt_no":1}
    record = point | data
    db.child("Call List").push(record)
    rkey = ""
    for key, value in result.items():
        rkey = key
        break
    db.child("New Leads").child(rkey).remove()

    global new_rec_num
    try:
        rec = newleadlist()
        if not rec:
            return redirect('/empty-newleads')
           
        point = rec[new_rec_num]
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
    except:
        return redirect('/empty-newleads')

    return render(request, "new-leads.html", {"email": email, "name": name, "phone": phone, "time": time, "source": source, "messages":"A cooldown of 18 hours has been added to previous lead"})

def NewNotAnswred(request):
    global new_rec_num

    result = db.child("New Leads").get()
    result = result.val()
    rec = get_New_List("New Leads")
    point = rec[0]
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {"Attempted":now,"status":"Not answered", "Attempt_no":1}
    record = point | data
    db.child("Call List").push(record)
    rkey = ""
    for key, value in result.items():
        rkey = key
        break
    db.child("New Leads").child(rkey).remove()

    return redirect('/services/call-leads/new-leads')

def NewNotIntrested(request):
    global new_rec_num
    new_rec_num = 0
    move_to_archive("Not intrested")
    return redirect('/services/call-leads/new-leads')
def NewInvalid(request):
    global new_rec_num
    move_to_archive("Invalid phone number")
    new_rec_num = 0

    return redirect('/services/call-leads/new-leads')

def CallList(request):
    global rec_num
    try:
        rec = get_Call_List()
        print(rec)
        point = rec[rec_num]
          # Iterate over dictionary items
        time = point["Attempted"]
        if hour_difference_from_now(time) > 18:
            email = point["Email"]
            name = point["Name"]
            phone = point["phone"]
            time = point["Created"]
            last_attempted = point["Attempted"]
            source = point["Platform"]
            return render(request, "call-list.html", {"email": email, "name": name, "phone": phone, "time": time, "source": source, "last_attempted":last_attempted})
        return redirect('/empty-call-list')
    except:
        return redirect('/empty-call-list')
    finally:
        return redirect('/empty-call-list')

def CallResult(request):
    
    return render(request, "call-result.html")

def Call(request):    
    return redirect("/")


def calendly(request):
    global rec_num
    try:
        result = db.child("Call List").get()
        result = result.val()
        rkey=""
        rec = get_Call_List()
        point = rec[rec_num]
        attempt_no = point["Attempt_no"]
        # phone = point["phone"]
        for key, value in result.items():
            rkey = key
            break
        attempt_no = attempt_no +1
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.child("Call List").child(rkey).update({"Attempt_no": attempt_no})
        db.child("Call List").child(rkey).update({"Attempted": now})
        db.child("Call List").child(rkey).update({"status": "Booked"})
        db.child("Archived").push(point)
        db.child("Call List").child(rkey).remove()
    
        return render(request, "calendly.html")
    except:
        return redirect('/empty-call-list')


def ResultLog(request):
    return render(request, "result-log.html")

def CallBackLater(request):
    global rec_num 
    try:
        
        result = db.child("Call List").get()
        result = result.val()
        rkey=""
        rec = get_Call_List()
        point = rec[rec_num]
        attempt_no = point["Attempt_no"]
        i=0
        for key, value in result.items():
            rkey = key
            if i== rec_num:
                break
            i = i+1
        attempt_no = attempt_no +1
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.child("Call List").child(rkey).update({"Attempt_no": attempt_no})
        db.child("Call List").child(rkey).update({"Attempted": now})
        db.child("Call List").child(rkey).update({"status": "Call back later"})
        num = point["Attempt_no"]
        if num >= 10:
            db.child("Archived").push(point)
            db.child("Call List").child(rkey).remove()
        else:
            rec_num = rec_num +1
        return redirect('/services/call-leads/call-list')
    except:
        return redirect('/empty-call-list')

def NotAnswered(request):
    global rec_num
    try:
        rec_num = rec_num +1
        result = db.child("Call List").get()
        result = result.val()
        rkey=""
        rec = get_Call_List()
        point = rec[rec_num]
        attempt_no = point["Attempt_no"]
        i = 0
        for key, value in result.items():
            rkey = key
            if i == rec_num:
                break
            i = i+1
        attempt_no = attempt_no +1
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.child("Call List").child(rkey).update({"Attempt_no": attempt_no})
        db.child("Call List").child(rkey).update({"Attempted": now})
        db.child("Call List").child(rkey).update({"status": "Not answred"})
        num = point["Attempt_no"]
        if num >= 10:
            db.child("Archived").push(point)
            db.child("Call List").child(rkey).remove()
        else:
            rec_num = rec_num +1
    
        return redirect('/services/call-leads/call-list')
    except:
        return redirect('/empty-call-list')
    

def NotIntrested(request):
    global rec_num
    try:
        result = db.child("Call List").get()
        result = result.val()
        rkey=""
        rec = get_Call_List()
        point = rec[rec_num]
        attempt_no = point["Attempt_no"]
        i = 0
        for key, value in result.items():
            rkey = key
            if i == rec_num:
                break
            i = i+1
        attempt_no = attempt_no +1
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.child("Call List").child(rkey).update({"Attempt_no": attempt_no})
        db.child("Call List").child(rkey).update({"Attempted": now})
        db.child("Call List").child(rkey).update({"status": "Not Intrested"})
        db.child("Archived").push(point)
        db.child("Call List").child(rkey).remove()   
        
        return redirect('/services/call-leads/call-list')
    except:
        return redirect('/empty-call-list')

def Invalid(request):
    global rec_num
    try:
        result = db.child("Call List").get()
        result = result.val()
        rkey=""
        rec = get_Call_List()
        point = rec[rec_num]
        attempt_no = point["Attempt_no"]
        # phone = point["phone"]
        for key, value in result.items():
            rkey = key
            break
        attempt_no = attempt_no +1
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.child("Call List").child(rkey).update({"Attempt_no": attempt_no})
        db.child("Call List").child(rkey).update({"Attempted": now})
        db.child("Call List").child(rkey).update({"status": "Invalid phone number"})
        db.child("Archived").push(point)
        db.child("Call List").child(rkey).remove()    
        return redirect('/services/call-leads/call-list')
    except:
        return redirect('/empty-call-list')
