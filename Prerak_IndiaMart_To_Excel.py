import json
import re
import pandas as pd
import urllib.request,urllib.parse,urllib.error
import ssl
from openpyxl import load_workbook
import os
from license import encrypt_message,decrypt_message,mobilecheck,keycheck,licenseVerification,timecheck
from functions import monthyear,path
import time
from eula import eulafile

if not os.path.isfile('C:/Users/Public/EULA.txt') :
    eulafile()

try :
    os.makedirs('C:/IndiaMart Excel/')
    print('\nWelcome to the "IndiaMart to Excel" software by Prerak Bhandari.\n')
    print('Guidelines :-\n')
    print('  1. All the data of Excel file will be stored in a folder under C:\n')
    print('  2. The Excel file name is given based on Month-Year of End Date.\n')
    print('  3. For every new Month-Year, a new Excel file will be created to make your Records easily accessible.\n')
    print('  4. If the Month-Year already exists, then a new sheet will be added to the file.\n')
    print('  5. It is adviced to run this software in a gap of at least 15 minutes as per IndiaMart norms.\n')
    print('  6. Please do not share your IndiaMart Key with anyone. It can be used to access your data.\n')
    print('  7. Your details will be protected using Advanced Encyption.\n')
    print('\n"IndiaMart Excel" folder created in "C:/IndiaMart Excel/"\n')
except :
    print('\nWelcome to the "IndiaMart to Excel" software by Prerak Bhandari.\n')
    print('You are using Advanced Encryption.')
    print('\n"IndiaMart Excel" folder exists in "C:/IndiaMart Excel"\n')
if not os.path.isfile('C:/Users/Public/IndiaMart_Mobile_Data.key'):
    datafile = open('C:/Users/Public/IndiaMart_Mobile_Data.key','w+')
    datafile.write('mobile:')
    print('\nData files created successfully.\nPlease enter your details.\n(This is a one time process.)\n')
else :
    datafile = open('C:/Users/Public/IndiaMart_Mobile_Data.key')
    dataread = datafile.read()
    if 'mobile:' in dataread : #already stored mobile number
        print("\nYou have been Automatically Logged Into IndiaMart.\n")
datafile.close()

serviceurl = 'https://mapi.indiamart.com/wservce/enquiry/listing/'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



GLUSR_MOBILE = None
GLUSR_MOBILE_KEY = None
GLUSR_MOBILE = mobilecheck()
GLUSR_MOBILE_KEY = keycheck()
print('Your Product Number is : ',os.popen("wmic diskdrive get SerialNumber").read().split()[1])
print()
try:
    expTIME = timecheck()
    if expTIME == 'License Expired.' :
        timefile = open('C:/Users/Public/Everything.key','rb')
        for line in timefile :
            seconds = time.time()
            exptimestr = decrypt_message(line)
            print('Your License has Expired on %s\nKindly renew your License\n'%exptimestr)
            timefile.close()
except:
    print('Error in Main Program : TC')
else :
    print('Your License is valid till : ',expTIME)
    print()

try:
    licenseVerification()
except:
    print('Error in Main Program : LV')

print('\nThe maximum difference of start date and end date should be 7 days.\nIf more than that is given ,then 7 days before end date will be considered.\n')

while True :
    print('To exit, press Enter.')
    Start_Time = input("Enter Start Date(DD-MM-YYYY) : ").upper()
    if len(Start_Time) < 1:
        break
    End_Time = input("Enter End Date(DD-MM-YYYY) : ").upper()
    print('\n')

    url = serviceurl + 'GLUSR_MOBILE/'+GLUSR_MOBILE+'/GLUSR_MOBILE_KEY/'+GLUSR_MOBILE_KEY+'/Start_Time/'+Start_Time+'/End_Time/'+End_Time+'/'

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()

    try:
        js = json.loads(data)
    except:
        js = None

    if "Error_Message" in js[0]:
        print(js[0]["Error_Message"])
        print('\n')
        continue

    df = pd.DataFrame(js)
    filename = monthyear(End_Time)+'.xlsx'
    filepath = path(filename)
    try :
        writer = pd.ExcelWriter(filepath ,mode='a')
        df.to_excel(writer, sheet_name = Start_Time+' to '+End_Time, index = False )
        writer.save()
    except :
        df.to_excel(filepath ,index = False, sheet_name = Start_Time+' to '+End_Time)

    print("\nExcel file successfully made.\n")
    path = "C:/IndiaMart Excel"
    path = os.path.realpath(path)
    os.startfile(path)
print('\nThank you for using this software.\n~Prerak Bhandari\n')
time.sleep(1.5)
