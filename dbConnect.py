#dbcnnect
from firebase_admin import storage
from uuid import uuid4
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import datetime
import sys, os
import subprocess
import requests

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/home/smartFarm/Desktop/project_final/plant.json')
# Initialize the app with a service account, granting admin privileges

proid = "smarfarm-137a3"
default_app = firebase_admin.initialize_app(cred, {'storageBucket': f"{proid}.appspot.com",'databaseURL': 'https://smarfarm-137a3-default-rtdb.firebaseio.com/'})
bucket = storage.bucket()

basename = "smr"
sfdb = db.reference('SmartFarm')
def dbstateupload(soil,state):
    sfdb.update({
        'soil':soil,
        'state':state,
    })
    print('sendfirebase1')  #once
def PointChange(Point):
    sfdb.update({
        "Point":Point,
    })
def returnModel():
    sfdb.update({
        "modelRun":False,
        })
def returnUnityC():
    sfdb.update({
        "motorRun":False,
        "LEDOnOff":False,
    })
def runnable():
    a = sfdb.get('Runnable')
    a= a[0]['Runnable']
    if a:
        sfdb.update({
        'Runnable':False,
        })
        return True
    else:
        return False
def dbread():
    print(sfdb.get())
    return sfdb.get()

def imageUpload(file):
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token}
    blob = bucket.blob('SmartFarm/' + file)
    blob.metadata = metadata
    blob.upload_from_filename(filename='/home/smartFarm/Desktop/project_final/image_store/' + file, content_type='image/jpeg')
    print('hello')
    print(blob.public_url)


#camera and image upload
def execute_camera():
    suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpeg'
    filename = "_".join([basename, suffix])
    sfdb.update({'image_name':filename})
    #subprocess.call("libcamera-jpeg --width 240 --height 240 -o /home/smartFarm/Desktop/project/image_store/{}".format(filename),shell=True)
    subprocess.call("libcamera-jpeg -o /home/smartFarm/Desktop/project_final/image_store/{}".format(filename),shell=True)
    
    imageUpload(filename)
    return filename

