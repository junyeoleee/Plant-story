import datetime
import urllib.request
from dbConnect import *
from gpiocontorl import *
from model import *
from soil import *

RunT= int(datetime.datetime.now().hour)
LEDONOFF = False

while True:
    nowHour=int(datetime.datetime.now().hour)
    runab = runnable()
    dbInfo = dbread()
    if ((RunT == nowHour) or runab):
        soilHum = soilread(0)
        if(dbInfo['Point']>=10):
            imgname = execute_camera()
            image_path = "/home/smartFarm/Desktop/project_final/image_store/{}".format(imgname)
            plantstate =modelrun(image_path)
            print(plantstate)
            PointChange(dbInfo['Point']-10)
            if 'Tomato' not in plantstate:
                plantstate = "normal"
                
        else:
            plantstate = "PointLack"
        dbstateupload(soilHum,plantstate)
        if (soilHum< 30 and dbInfo['Point']>=10):
            motorcontorl(10)
            PointChange(dbInfo['Point']-10)
        if (nowHour>=dbInfo['startTime'] and nowHour<= (dbInfo['startTime']+8)):
            LEDon()
            LEDONOFF =True
        else:
            LEDoff()
            LEDONOFF =False
        RunT =int(datetime.datetime.now().hour)+1
    if(dbInfo["LEDOnOff"]):
        returnUnityC()
        if(LEDONOFF):
            LEDoff()
            LEDONOFF=False
        else:
            PointChange(dbInfo['Point']-10)
            LEDONOFF=True
            LEDon()
    if(dbInfo["motorRun"]):
        PointChange(dbInfo['Point']-10)
        motorcontorl(10)
        returnUnityC()
    if(dbInfo["modelRun"] and dbInfo['Point']>=10):
        urllib.request.urlretrieve(f"https://firebasestorage.googleapis.com/v0/b/smarfarm-137a3.appspot.com/o/SmartFarm%2F{dbInfo['image_name']}?alt=media&token=a5a66687-f37d-4755-8267-575a1ee01134",f"/home/smartFarm/Desktop/project_final/image_store/{dbInfo['image_name']}")
        image_path = "/home/smartFarm/Desktop/project_final/image_store/{}".format(dbInfo['image_name'])
        plantstate =modelrun(image_path)
        PointChange(dbInfo['Point']-10)
        if 'Tomato' not in plantstate:
                plantstate = "normal"
        dbstateupload(30,plantstate)
        returnModel()
    
    time.sleep(20)
