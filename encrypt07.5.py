"""
Date: 6/7/2018
Author: Knowles, D.
This is python practice from doing python tutorials to help with
future work projects in which I will need to have a firm grasp of
python to help with data analysis
"""

# Version changes for each iteration
version_encrypt = '07.5'

from datetime import datetime
from math import ceil
from pyperclip import copy

def main():
    run_code = initialize()
    while True:
        if run_code == 'y':
            [message,total_iterations] = input_secret()
        elif run_code == 'r':
            message = final_message
        elif run_code == 'c':
            copy(final_message)
            break
        else:
            break
        final_message = encrypt(message,total_iterations)
        run_code = display_end_options()

def initialize():
    run_code = 'y'
    print('\n\nThis program encrypts messages using the derv'\
                  + version_encrypt +'  format.')
    return run_code

def is_integer(number):
        try:
            int(number)
            return True
        except ValueError:
            return False

def input_secret():  
    message = input('\nWhat is the secret message?\n')
    message = str(message)
    message = message + '                    '
    answer = 'x'
    answer = input("Would you like to auto-encrypt multiple times? [Y/N]\n")
    answer = answer.lower()
    while answer != 'y' and answer != 'n':
        answer = input("Invalid input. Enter either 'Y' or 'N'\n")
    if answer == 'n':
        total_iterations = 1
    else:
        total_iterations = input("Enter desired encryption iterations: \n")
        while is_integer(total_iterations) == False:
            total_iterations = input("Invalid input. Enter an integer number\n")
        total_iterations = int(total_iterations)
    return [message,total_iterations]

def display_iterations(final_message,verbose,total_iterations,auto_length,j):
    if verbose == True:
        print('\n\nStep %d: Redefine letters' % (j+2))
        print(final_message)
    elif total_iterations < 50 or \
        (total_iterations < 500 and (auto_length-1) % 10 == 0) or \
        (auto_length-1) % 100 == 0:
        print('\nIteration #%d' % ((total_iterations-auto_length) + 1))
        print(final_message)
    if auto_length == 1:
        print('\nThe above encrypted message is ready to send safely')

def display_end_options():
    print("\n\nEnter 'Y' to encrypt a new message,")
    print("Enter 'R' to re-encrypt message with same settings for added security,")
    print("Enter 'C' to copy the encrypted message to your clipboard and close")
    print("Enter anything else (or nothing) to close the program")
    run_code = input('')
    run_code = run_code.lower()
    return run_code

def encrypt(message,total_iterations):            
    auto_length = total_iterations
    if auto_length > 1:
        verbose = False
    else:
        verbose = True
        print('\n\nBeginning encryption of the following message: ')
        print(message)
    while auto_length > 0:
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
        # Build encryption key
        key = []
        key.append(int(encrypt_time_minute/5) + 2) #encryption key 1
        key.append(int(encrypt_time_micro/50000) + 3) # encryption key 2
        key.append(encrypt_time_year - 2008) # encryption key 3
        key.append(encrypt_time_month + 4) # encryption key 4
        key.append(int(encrypt_time_hour/2) + 5) # encryption key 5
        key.append(int(encrypt_time_day/3) + 3) # encryption key 6
        key.append(int(encrypt_time_second/15) + 2) # encryption key 7

        # iterate based on how many encryption keys exsist
        for j in range(len(key)): 
            jum_mess = []     # jumbled message
            for i in range(key[j]):
                jum_mess += [x for x in message[-i-1::-key[j]]]
            if verbose == True:
                print('\n\n\nStep %d: Jumble the message' % (j+1))
                print(''.join(jum_mess))
            message = jum_mess
            
        # Step 2: Reassign characters
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
            
        #append version to front of message
        new_message.append(version_encrypt + ' ')

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
        final_message = ''.join(new_message)

        display_iterations(final_message,verbose,total_iterations,auto_length,j)

        # Decrement the auto_length
        auto_length -= 1
        #print(auto_length)
        message = final_message

    return final_message

# this needs to be at the end of my code
if __name__ == "__main__":
    main()
