"""
Date: 6/7/2018
Author: Knowles, D.
This is python practice from doing python tutorials to help with
future work projects in which I will need to have a firm grasp of
python to help with data analysis
"""

# Version changes for each iteration
version_decrypt = '07.6'
filename = "encryption_IDs.txt"

from math import ceil
from pyperclip import copy
import enchant
eng = enchant.Dict("en_US")
from pathlib import Path
import os
import sys

def main():
    run_code = initialize()
    encryption_password = check_key_file()
    while True:
        if run_code == 'y':
            [secret,auto_mode] = input_secret()            
        elif run_code == 'r':
            secret = final_message
        elif run_code == 'c':
            copy(final_message)
            break
        else:
            break
        final_message = decrypt(secret,auto_mode)
        run_code = display_end_options()
        
def is_integer(number):
        try:
            int(number)
            return True
        except ValueError:
            return False
        
def is_float(number):
        try:
            float(number)
            return True
        except ValueError:
            return False     

def initialize():
    run_code = 'y'
    print('\n\nThis program decrypts code generated using the derv'\
                  + version_decrypt +'  format.')
    print('When inputing a message, be sure to include the beginning numbers')
    return run_code

def input_secret():
    secret = input('Input the message that you want to decrypt:\n')
    secret = str(secret)
    answer = 'x'
    answer = input("Would you like to auto-decrypt this message? [Y/N]\n")
    answer = answer.lower()
    while answer != 'y' and answer != 'n':
        answer = input("Invalid input. Enter either 'Y' or 'N'\n")
    if answer == 'n':
        auto_mode = False
    else:
        auto_mode = True
    return [secret,auto_mode]

def check_version(secret,num_decryption):
    version_encrypt = secret[0:4]
    if version_encrypt != version_decrypt:
        display_iterations(secret,False, num_decryption,False)
        print('\n\nWARNING: decryption version does not match the encryption version')
        print('The decryption version is ' + version_decrypt)
        print('The encyrption version was ' + version_encrypt)
        nothing = input("Press 'Enter' to continue anyways or 'Q' to quit\n")
        nothing = nothing.lower()
        if nothing == 'q':
            raise SystemExit
    broken_secret = secret.split(' ')
    secret = ' '.join(broken_secret[1:])
    return secret

def is_english(message_to_check):
    possible_words = message_to_check.split(' ')
    num_eng = 0
    for n in range(len(possible_words)):
        #print(possible_words[n])
        try:
            if eng.check(possible_words[n]) == True:
                if is_integer(possible_words[n]) == False:
                    if is_float(possible_words[n]) == False:
                        if len(possible_words[n]) > 2:
                            num_eng += 1
                            #print('Detected word: ' + possible_words[n])
        except ValueError:
            pass
    #print(num_eng/float(len(possible_words)))
    if num_eng/float(len(possible_words)) > 0.1:
        return True
    else:
        return False

def display_end_options():
    print("\n\nEnter 'Y' to decrypt a new message,")
    print("Enter 'R' to re-decrypt this message if still encrypted,")
    print("Enter 'C' to copy the decrypted message to your clipboard and close")
    print("Enter anything else (or nothing) to close the program")
    run_code = input('')
    run_code = run_code.lower()
    return run_code

def display_iterations(final_message,auto_mode,num_decryption,flag_working):
    if auto_mode == False or len(final_message) < 1500 or \
       (len(final_message) < 2500 and num_decryption % 10 == 0) or \
       (len(final_message) < 25000 and num_decryption % 100 == 0) or \
       (num_decryption % 1000 == 0):
        print('\nThis is the message after %d decryption(s):' % num_decryption)
        print(final_message)
        flag_working = True
    if flag_working == True and len(final_message) > 2500:
        print("\nWorking", end= ' ')
        flag_working = False
    if (len(final_message) < 25000 and len(final_message) > 2500) and num_decryption % 10 == 0:
        print('.', end = ' ')
    if (len(final_message) >= 2500) and num_decryption % 100 == 0:
        print('.', end = ' ')
    return flag_working
    
def decrypt(secret,auto_mode):
    display_result = False
    num_decryption = 0
    flag_working = True
    while True:
        secret = check_version(secret,num_decryption)
        if is_integer(secret[0:2]) == True:        
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
            if auto_mode == False:
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
                final_message = ''.join(unjumble_message)
                if auto_mode == False:
                    print('\n\nStep %d: Unjumble the message' % (2 + k))
                    print(final_message)
                clear_message = unjumble_message
            num_decryption += 1
            flag_working = display_iterations(final_message,auto_mode,num_decryption,flag_working)

            secret = final_message
            
        else:
            print("\nWARNING: you're message cannot be deciphered")
        if auto_mode == True:
            if is_english(final_message) == True:
                auto_mode = False
        if auto_mode == False:
            flag_working = display_iterations(final_message,auto_mode,num_decryption,flag_working)
            break

    return final_message

def check_key_file():
    # Creates file if a file of that name doesn't currently exsist
    try:
        f = open(os.path.join(sys.path[0], filename), "r+")
        print("Encryption ID file found successfully")
    except FileNotFoundError:
        f = open(filename,"w+")
        print("No file found. New file created successfully")
        f.close()
    while True:
        display_contents()
        switch_code = display_id_menu()
        if switch_code == 'n':
            new_encryption_id()
        elif switch_code == 'd':
            delete_encryption()
        elif is_integer(switch_code):
            [result,encryption_password] = use_encryption(int(switch_code))
            if result == True:
                return encryption_password
                break
        else:
            raise SystemExit
        
def display_contents():
    f = open(os.path.join(sys.path[0], filename), "r+")
    encryption_passwords = f.readlines()
    encryption_passwords = [x.strip() for x in encryption_passwords] 
    if encryption_passwords == '':
        print("\nNo encryption IDs found\n")
    else:
        print("\nEncryption keys:")
        new_list = list(range(len(encryption_passwords)))[::2]
        for x in new_list:
            print(str(int(x/2)+1) + ") " + encryption_passwords[x])
    f.close()

def new_encryption_id():
    f = open(os.path.join(sys.path[0], filename), "a")
    new_code_name = input("\nPlease enter the code name for the new ID:\n")
    new_code_name = new_code_name.lower()
    while new_code_name == '':
        new_code_name = input("Enter a code name:\n")
    f.write(new_code_name + "\n")
    new_id = input("\nPlease enter the new encryption ID:\n")
    new_id = new_id.lower()
    while len(new_id) != 12:
        new_id = input("Invalid input. Re-enter encryption key:\n")
    f.write(new_id + "\n")
    print("Encryption ID added.")
    f.close()

def delete_encryption():
    f = open(os.path.join(sys.path[0], filename), "r+")
    encryption_passwords = f.readlines()
    encryption_passwords = [x.strip() for x in encryption_passwords] 
    print("\nEnter the encryption key number that you wish to delete")
    index_to_delete = input('')
    print(is_integer(index_to_delete))
    while (is_integer(index_to_delete) == False or \
           encryption_index_exists(index_to_delete,encryption_passwords) == False):
        index_to_delete = input("Invalid entry. Please enter the integer number \
that corresponds to the encryption key that you wish to delete\n")
    f.close()
    f = open(os.path.join(sys.path[0], filename), "w")
    new_lines = list(range(len(encryption_passwords)))
    index_to_delete = int(index_to_delete)
    del new_lines[(index_to_delete-1)*2+1] # remove encryption password
    del new_lines[(index_to_delete-1)*2] # remove code name
    for line in list(new_lines):
        f.write(encryption_passwords[line] + '\n')
    f.close()

def encryption_index_exists(index,encryption_passwords):
    try:
        encryption_name = encryption_passwords[(int(index)-1)*2]
        return True
    except IndexError:
        print("\nWARNING: No Encryption ID with that number")
        return False

def display_id_menu():
    print("\nEnter 'N' to add a new encryption ID")
    print("Enter 'D' to delete an encryption key")
    print("Enter # of encryption key to use it to decode message")
    print("Enter anything else (or nothing) to close the program")
    switch_code = input('')
    switch_code = switch_code.lower()
    return switch_code
        
def use_encryption(index):
    f = open(os.path.join(sys.path[0], filename), "r+")
    encryption_passwords = f.readlines()
    encryption_passwords = [x.strip() for x in encryption_passwords] 
    if encryption_passwords == '':
        print("\nNo encryption IDs found\n")
    else:
        try:
            encryption_name = encryption_passwords[(index-1)*2]
            print("\nDecrypt with:")
            print(encryption_name)
            print('')
            encryption_password = encryption_passwords[(index-1)*2+1]
            f.close()
            return [True,encryption_password]
        except IndexError:
            print("\nWARNING: No Encryption ID with that number")
            f.close()
            return [False,0]
    
if __name__ == "__main__":
    main()
