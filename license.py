import re
from cryptography.fernet import Fernet
import os
import time
from datetime import datetime

#################################################################################################

def load_key():
    return open("C:/Users/Public/Secret.key", "rb").read()

def encrypt_message(message):

    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    #print(encrypted_message)
    return (encrypted_message)

def decrypt_message(encrypted_message):

    key = load_key()
    f = Fernet(key)
    try:
        decrypted_message = f.decrypt(encrypted_message)
        #print(decrypted_message.decode())
        return (decrypted_message.decode())
    except :
        return 'incorrectFormat'

###################################################################################################################



def mobilecheck() :
    file = open('C:/Users/Public/IndiaMart_Mobile_Data.key','r')
    for line in file :
        if re.search('^mobile:',line):
            try:
                mob = ((re.findall('[0-9].+',line))[0])
            except :
                mob = '0'
            if len(mob) == 10 :
                file.close()
                return mob
            else :
                file = open('C:/Users/Public/IndiaMart_Mobile_Data.key','a')
                while True :
                    mob = input('Enter 10-digits mobile number : ')
                    if re.match('[0-9]+$',mob) and len(mob) == 10:
                        file.write('%s\n' %mob)
                        print('\nMobile number saved successfully\n')
                        file.close()
                        with open('C:/Users/Public/Secret.key','wb') as secretfile :
                            secretfile.write(b'FDjIhMBPDrGC-ks6UyXUnAMS92FeHKYFMibzI0Z9tGM=')
                        #print('secret file made.')
                        key = input('Enter Key : ')
                        enckey = encrypt_message(key)
                        keyfile = open('C:/Users/Public/IndiaMart_Key_Data.key','wb')
                        keyfile.write(enckey)
                        print('\nMobile Key saved successfully.\n')
                        keyfile.close()

                        return mob
                    else:
                        print('\nInvalid mobile number. Please enter again.\n')


def keycheck() :
    file = open('C:/Users/Public/IndiaMart_Key_Data.key','rb')
    for line in file :
        origkey = decrypt_message(line)
        file.close()
        return (origkey)

###########################################################################################################

def timecheck() :
    if not os.path.isfile('C:/Users/Public/Everything.key'):

        timefile = open('C:/Users/Public/Everything.key','wb')
        seconds = time.time()
        licexp = seconds + 31536000

        oneyr = time.ctime(licexp)
        enctime = encrypt_message(oneyr)
        timefile.write(enctime)
        timefile.close()
        return oneyr
    else :
        timefile = open('C:/Users/Public/Everything.key','rb')
        for line in timefile :
            seconds = time.time()
            exptimestr = decrypt_message(line)
            exptimedt = time.strptime(exptimestr)
            exptimesec = time.mktime(exptimedt)
            if exptimesec >= seconds:
                timefile.close()
                return exptimestr
            else :
                timefile.close()
                return 'License Expired.'


#############################################################################################################
def licenseVerification() :

    if not os.path.isfile('C:/Users/Public/License.key') :
        flag = True
        while flag == True :
            exptime = timecheck()
            if exptime != 'License Expired.' :
                print('Your New License will expire on : ',exptime)
            l_key = input('Enter License Key : ')
            with open('C:/Users/Public/License.key','w') as newlicensefile :
                newlicensefile.write(l_key)
                newlicensefile.close()

            with open('C:/Users/Public/License.key','rb') as l_check :
                for line in l_check :
                    ddsn = os.popen("wmic diskdrive get SerialNumber").read().split()[1]
                    license = decrypt_message(line)
                    if license == 'Prerak'+ddsn+'MomoCartoonYellow'+exptime :           #1

                        print('License key verified.')
                        #timecheck()
                        flag = False

                    elif license == 'incorrectFormat':                                  #2
                        print('Incorrect format of license.')
                        seconds = time.time()
                        exptimedt = time.strptime(exptime)
                        exptimesec = time.mktime(exptimedt)
                        if exptimesec < seconds:
                            os.remove('C:/Users/Public/Everything.key')
                        break


                    else:                                                               #3
                        print('\nLicense key not correct')
                        print('Please enter correct license key again.\n')
                        seconds = time.time()
                        exptimedt = time.strptime(exptime)
                        exptimesec = time.mktime(exptimedt)
                        if exptimesec < seconds:
                            os.remove('C:/Users/Public/Everything.key')
                        break

    else :
        exptime = timecheck()

        ddsn = os.popen("wmic diskdrive get SerialNumber").read().split()[1]

        with open('C:/Users/Public/License.key','rb') as l_check :

            lolf = l_check.read()

            if len(lolf) < 1:
                l_check.close()
                os.remove('C:/Users/Public/Everything.key')
                os.remove('C:/Users/Public/License.key')

                licenseVerification()

            else:
                l_check.close()
                l_check = open('C:/Users/Public/License.key','rb')

                for line in l_check :

                    license = decrypt_message(line)

                    if license == 'Prerak'+ddsn+'MomoCartoonYellow'+exptime :

                        print('License verified.')

                    elif license == 'incorrectFormat':

                        print('Incorrect Format of License.')
                        l_check.close()
                        os.remove('C:/Users/Public/Everything.key')
                        os.remove('C:/Users/Public/License.key')

                        licenseVerification()

                    else:

                        print('License not Valid')
                        l_check.close()
                        os.remove('C:/Users/Public/Everything.key')
                        os.remove('C:/Users/Public/License.key')

                        licenseVerification()
                        break
                        
