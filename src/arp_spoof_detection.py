import subprocess, re
from time import sleep
import scapy.all as scapy


def determine_gatewayipandmac():
    ipconfig = subprocess.run(["ipconfig"], capture_output=True, text=True, shell=True)
    gateway_search = re.search(f"Default Gateway .*\s.*\d", ipconfig.stdout)
    gateway_string = ipconfig.stdout[gateway_search.span()[0]:  gateway_search.span()[1]]
    ip_search = re.search("([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})", gateway_string)
    ip = gateway_string[ip_search.span()[0]: ip_search.span()[1]]

    arp_a = subprocess.run(["arp", "-a"], capture_output=True, text=True, shell=True)
    ip_mac_search = re.search(f"\s{ip}\s.*", arp_a.stdout)
    mac_string = arp_a.stdout[ip_mac_search.span()[0]:  ip_mac_search.span()[1]]
    mac_search = re.search("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", mac_string)
    mac = mac_string[mac_search.span()[0]: mac_search.span()[1]]

    return ip, mac


def scanning_spoofed_mac(gateway_ip, gateway_mac):
    res3 = subprocess.run(["arp", "-a"], capture_output=True, text=True, shell=True)
    search_for_duplicates = re.findall(f".*{gateway_mac}", res3.stdout)
    attacker = ""

    # If we find more than one ARP entry , it means that someone is "pretending" to be the gateway/router .
    if len(search_for_duplicates) > 1:
        for i in range(len(search_for_duplicates)):
            x2 = re.search("([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})", search_for_duplicates[i])
            temp_ip = search_for_duplicates[i][x2.span()[0]: x2.span()[1]]
            
            if temp_ip != gateway_ip:
                attacker = temp_ip

        return attacker, True
    
    return attacker, False


gateway_ip, gateway_mac = determine_gatewayipandmac()
request = scapy.ARP(op=1, pdst=gateway_ip, psrc="192.168.1.30", hwdst=scapy.getmacbyip(gateway_ip))
reply = scapy.ARP(op=2, pdst=gateway_ip, psrc="192.168.1.30", hwdst=scapy.getmacbyip(gateway_ip))

while True:
    try:
        print(f"IP of gateway is : {gateway_ip} \nMAC of gateway is : {gateway_mac}")
        gateway_ip, gateway_mac = determine_gatewayipandmac()
        attacker, spoofingCheck = scanning_spoofed_mac(gateway_ip, gateway_mac)

        if spoofingCheck:
            scapy.send(reply, verbose = False)

            print(f"Warning ! {attacker} is spoofing his MAC to the default gateway !\nStarting ARP spoof prevention....")
            print("Gateway's TRUE MAC : ", scapy.sr1(request, verbose = False).getfieldval('hwsrc'))
        else:
            print("All good !")

        sleep(5)

    except KeyboardInterrupt:
        print("Stopping the checks.....")
        break