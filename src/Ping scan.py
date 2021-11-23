#The following script is a ping scan that allows us to detect "alive" devices or hosts in our network .
#Currently it only supports for a scan of max 256 hosts (/24 or 0-255) for ease and faster execution time (Warning : it's slow).
#It is currently supported only for Windows , some modifications have to happen to be supported in other OS.

import subprocess
import threading
import time

start_time = time.time()

#This function takes the initial string (input) and discards all the spaces , so we can make our job easier and more predictable.
def noSpaceString(ip_range):
    renewed_range = []
    for char in range(len(ip_range)):
        if ip_range[char] == ' ':
            pass
        else:
            renewed_range.append(ip_range[char])
    return ''.join(renewed_range)


#Function to store all the indexes of the dots. (We do this so we can isolate octets with confidence)
#Save each index to index_list and return its elements. We execute this function in the get_octets function .
def get_indexes(ip_range):
    index_list = []
    for i in range(len(ip_range)):
        if ip_range[i] == ".":
            index_list.append(i)

    #The slash character is for method '1' and the dash character is for method '2'.
    if method == '1':
        index_list.append(ip_range.index('/'))
    else:
        index_list.append(ip_range.index('-'))

    return index_list[0], index_list[1], index_list[2], index_list[3]


#In this function, we export the octets one by one as strings, we insert them in a list (octets) and after we convert all the values into integers we return it.
#I used several string methods to isolate the octets from the dots '.' and slash '/' or dash '-' (depending on the method that the user chooses).
#I also used the get_indexes (ip_range) function, which aims to give me the indexes of the dots, so that I can "find" the digits between the dots.

def get_octets(ip_range):
    octets = []
    ind1, ind2, ind3, ind_of_slash_or_dash = get_indexes(ip_range)

    oct1 = int(ip_range[0: ind1])
    oct2 = int(ip_range[ind1 + 1: ind2])
    oct3 = int(ip_range[ind2 + 1: ind3])
    oct4 = int(ip_range[ind3 + 1: ind_of_slash_or_dash])

    octets.extend([oct1, oct2, oct3, oct4])

    return octets


# Σε αυτή την συνάρτηση εξάγουμε το prefix length που μας έδωσε ο χρήστης . Παίρνωντας το ip range (ip_range) ως όρισμα , βρίσκουμε το prefix .

def get_prefix_or_end_address(ip_range, method):
    length = len(ip_range)
    if method == '1':
        x = ip_range.index('/')
    else:
        x = ip_range.index('-')

    return int(ip_range[x + 1: length])


# Συνάρτηση για τον έλεγχο λαθών χρήστη . Ελέγχουμε άμα έβαλε κάποιον άκυρο χαρακτήρα , άμα δεν έβαλε prefix length , άμα τα octets του ξεπερνάνε τα
# -επιτρεπόμενα όρια , άμα το prefix length που έβαλε είναι μεγαλύτερο του 32 ή μικρότερο του 24 και άμα ο γενικός πληθυσμός των χαρακτήρων είναι περι-
# -σσότεροι ή λιγότεροι από τι περιμένουμε .
# Για τώρα , δεν το έχω προγραμματίσει να υποστηρίζει prefixes μικρότερα από 24 για λόγους απλότητας και ευκολίας (δηλ. πρέπει να ελέγξουμε και να
# επεξεργάσουμε μόνο το τελευταίο octet) , και για να το τεστάρω στο LAN μου .

def check_for_errors():
    global prefix
    global end_address
    global octets
    global method
    valid_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '/', '.', '-']

    for j in range(len(ip_range)):

        if ip_range[j] not in valid_values:
            print("Not valid character found (*", ip_range[j], "*) , Please try again ....\n")
            return False

    if len(ip_range) > 18 or len(ip_range) < 9:
        print("More characters typed than expected , Please try again ....\n")
        return False

    if '-' in ip_range and '/' in ip_range:
        print("Not supported , Please try again ....")
        return False

    if '-' in ip_range:
        method = '2'
    elif '/' in ip_range:
        method = '1'
    else:
        print("No supported method identified , Please try again ....")
        return False

    #Exporting the 4 octets as integers in a list.
    octets = get_octets(ip_range)

    # Εξάγουμε το μέγεθος του prefix ως ακέραιο (ή το end address), θα το χρησιμοποιήσουμε για έλεγχο και για τον υπολογισμό των host που θα σκανάρουμε .
    # Αυτή την στιγμή δεν επιτρέπουμε τα prefix lengths μικρότερα των 24 για απλότητα και ευκολία .
    if method == '1':
        prefix = get_prefix_or_end_address(ip_range, method)
    else:
        end_address = get_prefix_or_end_address(ip_range, method)

    for j in range(0, 4):
        if octets[j] > 255 or octets[j] < 0:
            print("The input value of an octet is exceeding the limits of an IPv4 address , Please try again ....\n")
            return False

    if method == '1':

        if prefix < 24 or prefix > 32:
            print("The specified prefix length is incorrect or not supported , Please try again ....\n")
            return False

    if method == '2':

        if octets[3] > end_address:
            print("Invalid syntax , Please try again ...\n")
            return False

        if end_address > 255 or end_address < 0:
            print("The end address is exceeding the limits , Please try again ...\n")
            return False

    return True


def init_process():
    global ip_range

    #Getting the input string of the user , which is the ip range that he wishes to scan .
    ip_range = str(
        input("Type the IPv4 address range that you wish to scan following these two methods : ( 192.168.1.0/24 )   "
              "or   ( 192.168.1.0-255 )    :"))

    #We remove all the spaces added by the user by mistake, in order to make the job easier (because of the indexes) and more predictable.
    ip_range = noSpaceString(ip_range)


#This the fuction that we ping from our system (Only for Windows10). After the ping, we
#check the returncode and its message to find out what the result was . Returncode 0 means that a command was executed successfully,
#but for some reason in Windows the messages "Destination host unreachable", "Destination net unreachable" and a successful echo reply, have
#all returncode 0 (unlike linux). For this reason , I also checked their output(stdout). The addresses that responded successfully to the pings
#are listed in the active_ips list.
def scanning_process(first_address , last_address):
    global active_ips

    for j in range(first_address , last_address):

        #if we exceed the limits of the last octet , abort .
        if j > 255 :
            break

        #The current address to be scanned.
        address = str(octets[0]) + "." + str(octets[1]) + "." + str(octets[2]) + "." + str(j)

        #This is the actual command that runs on the background for all the ip addresses (ping "192.168.1.1" -n 3)
        res = subprocess.run( ["ping", address, "-n", '3', ] , capture_output=True, text=True )

        if res.returncode == 0 and (res.stdout.count("Destination host unreachable")) > 1:
            print(address, "is unreachable!")

        elif res.returncode == 0 and (res.stdout.count("Destination net unreachable")) > 1:
            print("The network of ", address, "is unreachable!")

        elif res.returncode == 0:
            print(address, "is responsive!")
            active_ips.append(address)

        else:
            print("Ping to " + address, "failed!")


# Συνάρτηση για να ταξινομήσουμε την λίστα των ενεργών host από την λίστα active_ips . Μερικά threads/processes τελειώνουν πιο γρήγορα από
# τις προηγούμενες τους , γι'αυτό πρέπει να ταξινόμησουμε την λίστα . Αυτή η συνάρτηση είναι προαιρετική .
def bubble_sort():
    global active_ips
    last_octets = []

    for ip in range(len(active_ips)):
        temp_string = active_ips[ip]
        ind3 = temp_string.rindex('.')
        oct4 = temp_string[ind3 + 1: len(temp_string)]
        last_octets.append(int(oct4))

    for i in range(len(active_ips)):

        for j in range(0, len(active_ips) - i - 1):

            if last_octets[j] > last_octets[j + 1]:

                holder = last_octets[j]
                last_octets[j] = last_octets[j + 1]
                last_octets[j + 1] = holder
                holder = active_ips[j]
                active_ips[j] = active_ips[j + 1]
                active_ips[j + 1] = holder


#Method '1' is the prefix method (i.e. 192,168.1.0/24) , while method '2' is the range method (i.e. 192,168.1.0 - 255)

method = ''
ip_range = ''
prefix = -1
end_address = -1
octets = []
active_ips = []
threads = []

print("\n\n[PING SCAN]\n\n")
init_process()

while check_for_errors() == False:
    init_process()



if method == '1':

    if octets[3] + pow(2, 32 - prefix) > 256:
        count = 256 - octets[3]
    else:
        count = pow(2, 32 - prefix)


elif method == '2':

    if end_address > octets[3]:
        count = end_address - octets[3] + 1
    elif end_address < octets[3]:
        count = octets[3] - end_address
    else:
        count = 1

else:
    count = 0


print("Scanning ", count, "host(s).\n")

if count < 8 :
    increment = 1
elif count % 8 == 0:
    increment = int(count / 8)
else:
    increment = int(count / 8) + 1


start = octets[3]
finish = start + increment


if count < 8 :

    for i in range(count):

        print("Start:", start)

        print("Increment:", increment)

        print("Telos:", finish)

        t = threading.Thread(target=scanning_process, args=(start, finish,))
        t.start()
        threads.append(t)

        start = finish
        finish += increment

    for thread in threads:
        thread.join()


else:

    for i in range(8):

        print("Start:",start)

        print("Increment:",increment)

        print("Telos:",finish)

        t = threading.Thread(target=scanning_process , args=(start,finish,))
        t.start()
        threads.append(t)

        start = finish
        finish += increment

    for thread in threads:
        thread.join()



print("\n\n\n\n")
print("[ACTIVE HOSTS]\n")

bubble_sort()

for i in range(0, len(active_ips)):
    print(active_ips[i])

print('\n', len(active_ips), "active host(s) detected out of", count)
print("--- %s seconds ---" % (time.time() - start_time))