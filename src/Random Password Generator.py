import string
import random

def input_process(total_length , use_of_digits , use_of_punctuations):

    total_length = input("Set your desired character length : ")
    use_of_digits = str(input("Would you like to add digits to your password ? (y/n)  :").lower())
    use_of_punctuations = str(input("Would you like to add punctuations to your password ? (y/n)  :").lower())

    return total_length , use_of_digits , use_of_punctuations

def error_checking( length , digits , punctuations ):

    try:
        length = int(length)
    except ValueError:
        print("Invalid type of variable detected !\nPlease Try Again .")
        return False

    #Feel free to adjust the max character length (currently 128) .
    if length < 0 or length > 128 :
        print("Invalid character length !\nPlease Try Again .")
        return False

    if digits != 'n' and digits != 'no' and digits != 'y' and digits != 'yes' :
        print("Invalid answer for use of digits detected !\nPlease Try Again .")
        return False

    if punctuations != 'n' and punctuations != 'no'  and punctuations != 'y' and punctuations != 'yes' :
        print("Invalid answer for use of punctuations detected !\nPlease Try Again .")
        return False

    return True

def determine_password( total_length , use_of_digits , use_of_punctuations ):

    char_list = []

    if (use_of_digits == 'y' or use_of_digits == 'yes') and (
            use_of_punctuations == 'y' or use_of_punctuations == 'yes'):

        for i in range( int(total_length) ):
            char_list.append(string.printable[random.randint(0, 93)])

    elif (use_of_digits == 'y' or use_of_digits == 'yes') and \
            (use_of_punctuations == 'n' or use_of_punctuations == 'no'):

        for i in range( int(total_length) ):
            char_list.append(string.printable[random.randint(0, 61)])

    elif (use_of_digits == 'n' or use_of_digits == 'no') and \
            (use_of_punctuations == 'y' or use_of_punctuations == 'yes'):

        for i in range( int(total_length) ):
            char_list.append(string.printable[random.randint(10, 93)])

    else:
        for i in range( int(total_length) ):
            char_list.append(string.printable[random.randint(10, 61)])

    return ''.join(char_list)


def main_program(total_length , use_of_digits , use_of_punctuations):

    satisfied = True
    print("[RANDOM PASSWORD GENERATOR]")

    total_length , use_of_digits , use_of_punctuations = input_process( total_length , use_of_digits , use_of_punctuations )

    while not ( error_checking( total_length , use_of_digits , use_of_punctuations ) ) :
        total_length , use_of_digits , use_of_punctuations = input_process( total_length , use_of_digits , use_of_punctuations )

    while satisfied == True:
        print("[PASSWORD]\n", determine_password( total_length , use_of_digits , use_of_punctuations ))
        satisfied = str(input("Would you like to compute a new password (y/n) :").lower())
        while satisfied[0] != 'y' and satisfied[0] != 'n':
            satisfied = str(input("Sorry , didn't catch that (y/n) :").lower())
        if satisfied[0] == 'y':
            satisfied = True
        elif satisfied[0] == 'n':
            satisfied = False




total_length = 0
use_of_digits = 'n'
use_of_punctuations = 'n'
restart = True

while restart == True:
    print("\n\n\n")
    main_program( total_length , use_of_digits , use_of_punctuations )
    restart = input("Restart ? (y/n) :")
    while restart[0] != 'y' and restart[0] != 'n':
        restart = str(input("Sorry , didn't catch that (y/n) :").lower())
    if restart[0] == 'y':
        restart = True
    elif restart[0] == 'n':
        restart = False
