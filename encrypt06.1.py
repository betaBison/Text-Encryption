"""
Date: 6/7/2018
Author: Knowles, D.
This is python practice from doing python tutorials to help with
future work projects in which I will need to have a firm grasp of
python to help with data analysis
"""

version = '07.1'

from datetime import datetime
from math import ceil
from pyperclip import copy
input_code = 'y'
while input_code == 'y' or input_code == 'r':

    if input_code == 'r':
        message = final_message
    else:
        print('\n\nThis program encrypts messages using the derv'\
              + version +'  format.')
        try:
            message = input('What is the secret message? ')
            message = str(message)
        except:
            import atexit
            atexit.register(input, 'Press Enter to continue...')
            raise # Reraise the exception
        print('\n\nBeginning encryption of the following message: ')
        print(message)
        message = message + '                    '

    # Time data 
    encrypt_time = datetime.now()
    # Change the time to writable objects to help w/ debugging
    encrypt_time_year = encrypt_time.year   #[2018,9999]
    encrypt_time_month = encrypt_time.month  #[1:12]
    encrypt_time_day = encrypt_time.day    #[1:31]
    encrypt_time_hour = encrypt_time.hour   #[1:24]
    encrypt_time_minute = encrypt_time.minute #[1:60]
    encrypt_time_second = encrypt_time.second #[1:60]
    encrypt_time_micro = encrypt_time.microsecond #[1:999999]

    '''
    # Standard numbers to help with debugging
    encrypt_time_year = 2018   #[2018,9999]
    encrypt_time_month = 6  #[1:12]
    encrypt_time_day = 12    #[1:31]
    encrypt_time_hour = 11   #[1:24]
    encrypt_time_minute = 58 #[1:60]
    encrypt_time_second = 14 #[1:60]
    encrypt_time_micro = 92432 #[1:999999]
    # List of all ASCII characters in order
    #  !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
    '''

    # Step 1: Jumble message
    #print('The minute = %s' % encrypt_time_minute)
    key = []
    key.append(int(encrypt_time_minute/5) + 2) #encryption key 1
    key.append(int(encrypt_time_micro/50000) + 3) # encryption key 2
    key.append(encrypt_time_year - 2008) # encryption key 3
    key.append(encrypt_time_month + 4) # encryption key 4
    key.append(int(encrypt_time_hour/2) + 5) # encryption key 5
    key.append(int(encrypt_time_day/3) + 3) # encryption key 6
    key.append(int(encrypt_time_second/15) + 2) # encryption key 7
    #print('The key is %s' % key)

    for j in range(len(key)): 
        jum_mess = []     # jumbled message 1
        for i in range(key[j]):
            jum_mess += [x for x in message[-i-1::-key[j]]]
        #print('The key = %d' % key[j])
        print('\n\n\nStep %d: Jumble the message' % (j+1))
        print(''.join(jum_mess))
        message = jum_mess
        
        

    new_message = []
    new_num_list = []
    for n in jum_mess:
        old_num = ord(n)       #convert to ASCII number [32:126]
        new_num = old_num
        new_num += encrypt_time_month
        new_num -= encrypt_time_day
        new_num += encrypt_time_hour
        new_num -= encrypt_time_minute
        new_num += (encrypt_time_year - 2020)
        new_num += (encrypt_time_second - 30)          #DON'T CHANGE THIS (for space detection)
        # keep the character within the normal readable boundaries
        while new_num < 32:
            new_num += 95
        while new_num > 126:
            new_num -= 95
        new_num_list.append(new_num)
        
    # Check to see if the last character is a space
    if new_num_list[-1] == 32:
        # if it is then fix it so it's not a problem
        new_num_list = [x + 1 for x in new_num_list]
        encrypt_time_second += 1

    #append timestamp to start of message
    timestamp = '%02d%04d%02d%02d%02d%02d%06d' % \
                (encrypt_time_second,encrypt_time_year,encrypt_time_month, \
                 encrypt_time_day,encrypt_time_minute,encrypt_time_hour, \
                 encrypt_time_micro)     
    new_message.append(timestamp)

    #append each letter to the message
    for number in new_num_list:
        # keep the character within the normal readable boundaries
        while number < 32:
            number += 95
        while number > 126:
            number -= 95    
        new_char = chr(number)
        new_message.append(new_char)

    print('\n\nStep %d: Redefine letters' % (j+2))
    print('The following encrypted message is ready to send safely')
    print('and has been copied to the clipboard:\n')
    final_message = ''.join(new_message)
    print(final_message)
    copy(final_message)

    print("\n\nEnter 'Y' to encrypt a new message,")
    print("Enter 'R' to re-encrypt this message for added security,")
    input_code = input("Enter anything else (or nothing) to close the program: ")
    input_code = input_code.lower()


