import os
def eulafile() :
    if not os.path.isfile('C:/Users/Public/EULA.txt') :
        feula = open('C:/Users/Public/EULA.txt','w')
        feula.write('https://www.eulatemplate.com/live.php?token=X3kYxUIHMz78xZo9wIz11jptwgmiV2PS')
        feula.close()
        print('\nYour End-User License Agreement(EULA) is stated at : https://bit.ly/30LCDAH\n')
        while True:
            accept = input('To ACCEPT, press "y" : ').upper()
            if accept == 'Y' :
                print('You can proceed.')
                break
