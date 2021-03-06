"""
Date: 6/7/2018
Author: Knowles, D.
This is python practice from doing python tutorials to help with
future work projects in which I will need to have a firm grasp of
python to help with data analysis
"""

# Version changes for each iteration
version_decrypt = '07.2'

from math import ceil
from pyperclip import copy

def main():
    [run_code,final_message] = initialize()
    while run_code != 'q':
        if run_code == 'y':
            secret = input_secret()            
        elif run_code == 'r':
            secret = final_message
        elif run_code == 'c':
            copy(final_message)
            break
        else:
            break
        [run_code,final_message] = decrypt(secret)       
        

def initialize():
    run_code = 'y'
    final_message = []
    print('\n\nThis program decrypts code generated using the derv'\
                  + version_decrypt +'  format.')
    print('When inputing a message, be sure to include the beginning numbers')
    return [run_code,final_message]

def input_secret():
    secret = input('Input the message that you want to decrypt: ')
    secret = str(secret)
    return secret

def check_version(secret):
    version_encrypt = secret[0:4]
    if version_encrypt != version_decrypt:
        print('\n\nWARNING: decryption version does not match the encryption version')
        print('The decryption version is ' + version_decrypt)
        print('The encyrption version was ' + version_encrypt)
        nothing = input('Press Enter to continue anyways')
    broken_secret = secret.split(' ')
    secret = ' '.join(broken_secret[1:])
    return secret

def decrypt(secret):
    secret = check_version(secret)    
    encrypt_second = int(secret[0:2])
    encrypt_year = int(secret[2:6])
    encrypt_month = int(secret[6:8])
    encrypt_day = int(secret[8:10])
    encrypt_minute = int(secret[10:12])
    encrypt_hour = int(secret[12:14])
    encrypt_micro = int(secret[14:20])

    clear_message = []
    secret_num_list = []
    for n in secret[20:]:
        secret_num = ord(n)
        secret_num_list.append(secret_num)
    #print(secret_num_list)
    for n in secret_num_list:
        clear_num = n
        clear_num -= (encrypt_second - 30)
        clear_num -= (encrypt_year - 2020)
        clear_num += encrypt_minute
        clear_num -= encrypt_hour
        clear_num += encrypt_day
        clear_num -= encrypt_month

        while clear_num < 32:
            clear_num += 95
        while clear_num > 126:
            clear_num -= 95
        clear_char = chr(clear_num)
        clear_message.append(clear_char)
    print('\n\nStep 1: Reassign characters')
    print(''.join(clear_message))
    # Unjumble the message
    #print(encrypt_minute)
    key = []
    key.append(int(encrypt_second/15) + 2) #encryption key 7
    key.append(int(encrypt_day/3) + 3) #encryption key 6
    key.append(int(encrypt_hour/2) + 5) #encryption key 5
    key.append(encrypt_month + 4) #encryption key 4
    key.append(encrypt_year - 2008) #encryption key 3
    key.append(int(encrypt_micro/50000) + 3) #encryption key 2
    key.append(int(encrypt_minute/5) + 2) #encryption key 1
    for k in range(len(key)):
        items_per_group = len(clear_message)/float(key[k])
        items_per_group = ceil(items_per_group)
        #print(items_per_group)
        num_not_ful = (key[k] * items_per_group) - len(clear_message)
        #print(num_not_ful)
        unjumble_dict = {}
        #print('The key is %s and value is %s' % (k,key[k]))
        # Creates dictionary of word groups
        for i in range(key[k]):
            #print('Num_not full = %d and i = %d' % (num_not_ful,i))
            if i < num_not_ful:
                num_first = i*(items_per_group-1)
                for j in range(items_per_group-1):
                    if i in unjumble_dict.keys():
                        unjumble_dict[i].append(clear_message[-1-j-num_first])
                    else:
                        unjumble_dict[i] = [clear_message[-1-j-num_first]]
                    #print('IF LOOP')
                    #print(unjumble_dict)
            else:
                num_first = num_not_ful*(items_per_group-1)
                num_sec = (i - num_not_ful)*items_per_group
                for j in range(items_per_group):
                    if i in unjumble_dict.keys():
                        unjumble_dict[i].append(clear_message[-1-j-num_first-num_sec])
                    else:
                        unjumble_dict[i] = [clear_message[-1-j-num_first-num_sec]]
                    #print('ELSE LOOP')
                    #print(unjumble_dict)
        #print(unjumble_dict)
        unjumble_message = []
        for i in range(key[k]):
            if len(unjumble_dict[i]) == items_per_group:
                unjumble_message.append(unjumble_dict[i][0])
                del unjumble_dict[i][0]
            #print(unjumble_message)
        for j in range(items_per_group-1):
            for i in range(key[k]):
                unjumble_message.append(unjumble_dict[i][j])
                #print(unjumble_message)
        #print(unjumble_message)
        print('\n\nStep %d: Unjumble the message' % (2 + k))
        final_message = ''.join(unjumble_message)
        print(final_message)
        clear_message = unjumble_message
    print('\nThis is the decrypted message')
    print('and has been copied to the clipboard:')
    print(final_message)
    

        
    print("\n\nEnter 'Y' to decrypt a new message,")
    print("Enter 'R' to re-decrypt this message if still encrypted,")
    print("Enter 'C' to copy the decrypted message to your clipboard and close")
    print("Enter anything else (or nothing) to close the program")
    run_code = input('')
    run_code = run_code.lower()

    return [run_code,final_message]

if __name__ == "__main__":
    main()
