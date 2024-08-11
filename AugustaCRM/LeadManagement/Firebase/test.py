import pyrebase
from datetime import datetime

import os

FIREBASE_CONFIG = {
    'apiKey': str(os.getenv('FIREBASE_API_KEY')),
    'authDomain': str(os.getenv('FIREBASE_AUTH_DOMAIN')),
    'databaseURL': "https://augusta-crm-95afd-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'projectId': str(os.getenv('FIREBASE_PROJECT_ID')),
    'storageBucket': str(os.getenv('FIREBASE_STORAGE_BUCKET')),
    'messagingSenderId': str(os.getenv('FIREBASE_MESSAGING_SENDER_ID')),
    'appId': str(os.getenv('FIREBASE_APP_ID')),
    'measurementId': str(os.getenv('FIREBASE_MEASUREMENT_ID')),
}

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth_fb = firebase.auth()
db = firebase.database()

now = datetime.now()
data = {"currenttimemillis":"12:12:08.76", "name":"Rishi", "email": "rishidwd29@gmail.com", "phone": "+9156473126", "lead_create_time/date": "current", "status": "pending"}
db.child("call_list").push(data)
# point=db.child("leads_details").child("email").get()
# # point= db.child("local_test").child("lead_details").child("email").get()
# email = point.val()
# print(email)