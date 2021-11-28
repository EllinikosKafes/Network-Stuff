import subprocess, threading, time


def noSpaceString(ip_range):
    return ip_range.replace(' ', '')


# Function to store all the indexes of the dots. (We do this so we can isolate octets with confidence)
# Save each index to index_list and return its elements. We execute this function in the get_octets function .
def get_indexes(ip_range, method):
    index_list = []
    
    for i in range(len(ip_range)):
        if ip_range[i] == ".":
            index_list.append(i)

    # The slash character is for method '1' and the dash character is for method '2'.

    if method == '1':
        index_list.append(ip_range.index('/'))
    else:
        index_list.append(ip_range.index('-'))

    return index_list[0], index_list[1], index_list[2], index_list[3]


def get_octets(ip_range, method):
    octets = []
    ind1, ind2, ind3, index_of_slash_or_dash = get_indexes(ip_range, method)

    oct1 = int(ip_range[0: ind1])
    oct2 = int(ip_range[ind1 + 1: ind2])
    oct3 = int(ip_range[ind2 + 1: ind3])
    oct4 = int(ip_range[ind3 + 1: index_of_slash_or_dash])

    octets.extend([oct1, oct2, oct3, oct4])

    return octets


def get_prefix_or_end_address(ip_string, method):
    length = len(ip_string)
    
    if method == '1':
        return int(ip_string[ip_string.index('/') + 1: length])
    
    return int(ip_string[ip_string.index('-') + 1: length])


# This function checks for input errors, it only checks for invalid characters, missing prefix length, allowed limits, prefix length limits
def check_for_errors(ip_range, speed):
    valid_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '/', '.', '-']
    prefix = -1
    end_address = -1

    try:
        speed = int(speed)
    except ValueError:
        print("This is not a supported speed , Please try again...")
        return False

    if speed not in [1, 2, 3]:
        print("This is not a supported speed , Please try again...")
        return False

    for j in range(len(ip_range)):
        if ip_range[j] not in valid_values:
            print("Not valid character found ('", ip_range[j], "') , Please try again ....\n")
            return False

    if len(ip_range) > 18 or len(ip_range) < 9:
        print("More characters typed than expected , Please try again ....\n")
        return False
    elif '-' in ip_range and '/' in ip_range:
        print("Not supported , Please try again ....")
        return False

    # Determine which method is being used .
    if '-' in ip_range:
        method = '2'
    elif '/' in ip_range:
        method = '1'
    else:
        print("No supported method identified , Please try again ....")
        return False

    # Exporting the 4 octets as integers in a list.
    octets = get_octets(ip_range, method)


    if method == '1':
        prefix = get_prefix_or_end_address(ip_range, method)
    else:
        end_address = get_prefix_or_end_address(ip_range, method)

    for j in range(4):
        if octets[j] > 255 or octets[j] < 0:
            print("The input value of an octet is exceeding the limits of an IPv4 address , Please try again ....\n")
            return False

    if method == '1':
        if prefix < 24 or prefix > 32:
            print("The specified prefix length is incorrect or not supported , Please try again ....\n")
            return False
    elif method == '2':
        if octets[3] > end_address:
            print("Invalid syntax , Please try again ...\n")
            return False
        elif end_address > 255 or end_address < 0:
            print("The end address is exceeding the limits of an IPv4 address , Please try again ...\n")
            return False


    return method , octets , prefix , end_address


def init_process():
    ip_range = input("Type the IPv4 address range that you wish to scan following these two methods : ( 192.168.1.0/24 )   "
              "or   ( 192.168.1.0-255 )    : ")

    # We remove all the spaces added by the user by mistake, in order to make the job easier (because of the indexes)
    # and more predictable.
    ip_range = noSpaceString(ip_range)
    speed = input("Choose speed ( 1 , 2 , 3 ): ")

    return ip_range, speed


# This function is what actually finds if a host is active or not with the ping command
def scanning_process(first_address, last_address ):
    global active_ips

    for j in range(first_address, last_address):

        # fail conditions
        if j > 255:
            break
        elif method == '2' and j > end_address:
            break

        # Check active hosts with the ping command
        address = str(octets[0]) + "." + str(octets[1]) + "." + str(octets[2]) + "." + str(j)
        res = subprocess.run(["ping", address, "-n", '3', ], capture_output=True, text=True)

        if res.returncode == 0 and (res.stdout.count("Destination host unreachable")) > 1:
            print(address, "is unreachable!")
        elif res.returncode == 0 and (res.stdout.count("Destination net unreachable")) > 1:
            print("The network of ", address, "is unreachable!")
        elif res.returncode == 0:
            print(address, "is responsive!")
            active_ips.append(address)
        else:
            print("Ping to " + address, "failed!")


def startThreads(totalThreads, start, finish):
    for i in range(totalThreads):
        t = threading.Thread(target=scanning_process, args=(start, finish,))
        t.start()
        threads.append(t)

        start = finish
        finish += increment

    for thread in threads:
        thread.join()


# Sort the active hosts in ascending order
def bubble_sort(active_ips):
    last_octets = []

    for ip in active_ips:
        temp_string = ip
        last_dot_index = temp_string.rindex('.')
        oct4 = temp_string[last_dot_index + 1: len(temp_string)]
        last_octets.append(int(oct4))

    for i in range(len(active_ips)):
        for j in range(0, len(active_ips) - i - 1):
            if last_octets[j] > last_octets[j + 1]:
                last_octets[j], last_octets[j + 1] = last_octets[j + 1], last_octets[j]
                active_ips[j], active_ips[j + 1] = active_ips[j + 1], active_ips[j]                

    return active_ips


# Method '1' is the prefix method (e.g. 192,168.1.0/24) , while method '2' is the range method (e.g. 192.168.1.0 - 255)

method = ''
ip_range = ''
speed = 0
prefix = -1
end_address = -1
octets = []
active_ips = []
threads = []
print("\n\n[PING SCAN]\n\n")

ip_range,speed = init_process()
while check_for_errors(ip_range , speed) == False:
    ip_range, speed = init_process()

method , octets , prefix , end_address = check_for_errors(ip_range , speed)


start_time = time.time()

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

if int(speed) == 1:
    if count < 8:
        increment = 1
    elif count % 8 == 0:
        increment = int(count / 8)
    else:
        increment = int(count / 8) + 1


elif int(speed) == 2:
    if count < 16:
        increment = 1
    elif count % 16 == 0:
        increment = int(count / 16)
    else:
        increment = int(count / 16) + 1

else:
    if count < 32:
        increment = 1
    elif count % 32 == 0:
        increment = int(count / 32)
    else:
        increment = int(count / 32) + 1


start = octets[3]
finish = start + increment
totalThreads = 0;


if int(speed) == 1:
    startThreads(8, start, finish)
elif int(speed) == 2:
    startThreads(16, start, finish)
else:
    startThreads(32, start, finish)


print("\n\n\n\n[ACTIVE HOSTS]\n")

active_ips = bubble_sort(active_ips)

for ip in active_ips:
    print(ip)

print('\n', len(active_ips), "active host(s) detected out of", count)
print("--- %s seconds ---" % (time.time() - start_time))
