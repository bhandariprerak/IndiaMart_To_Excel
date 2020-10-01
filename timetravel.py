# import time
# from datetime import datetime
import os
# seconds = time.time()
# print('Seconds epoch time = ',seconds)
# local_time = time.ctime(seconds)
# print('Local time = ',local_time)
#
# print('this is printed immediately')
# #time.sleep(2)
# print('this is printed after 2 seconds')
#
# now = datetime.now()
#
# print(now)
# # dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# print("date and time =", dt_string)
id = os.popen("wmic diskdrive get serialnumber").read().split()[-1]
print(id)

# import rsa
# pubkey, privkey = rsa.newkeys(512)
# print(pubkey,privkey)
# When a user purchases, generate a license key:

# data = 'user@email.com'
# signature = rsa.sign(data.encode('utf-8'), privkey, 'SHA-1')
# from base64 import b64encode
# print(data + '\n' + b64encode(signature).decode('ascii'))

from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("license.txt", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    return open("license.txt", "rb").read()

def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    print('your encrypted message is : ',encrypted_message)
    return (encrypted_message)

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    try:
        decrypted_message = f.decrypt(encrypted_message)
        print('decrypted message is : ',decrypted_message.decode())
        #return (decrypted_message.decode())
    except :
        print("error in encrydecry/decrypt_message")

msg = input('enter your message : ')
encmsg = encrypt_message(msg)
decrypt_message(encmsg)
