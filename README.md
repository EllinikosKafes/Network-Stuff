# Network-Stuff

This repository is meant for networking tools written in python 3. 

<br>

## ping_scan

Ping scan is a tool that searches all available hosts in a given network and prints out to the terminal what address is currently active or not by, as the name implies, pinging them.

<br>

**Ping scan uses the following libraries**

- subprocess
- threading
- time


<br>

## arp_spoof

Arp spoof is a simple python script that allows you to 'trick' the victim into thinking that you are the router , giving him (the victim) your own MAC and also 'tricking' the router into thinking that you are in fact the victim . 
This attack is also known as MITM (man-in-the-middle) attack , because we place ourselves in the middle of a communication.
Although this tool is not harmful overall , please do not use it to spy or steal data from other hosts .

<br>

**Arp spoof uses the following libraries**

- scapy
- time

<br>

\**Install scapy before executing the script : pip install scapy*

<br>

## arp_spoof_detection

Arp spoof detection detects (obviously) if you are being given a false Gateway MAC address , by checking your ARP table . If you are in fact being attacked by arp_spoofing , the script will try to give the gateway/router your valid credentials (your ip and mac address) 
with a makeshift ARP reply and also request its correct MAC address with a makeshift ARP request .

<br>

**Arp spoof detection uses the following libraries**

- subprocess
- re (Regular Expression)
- scapy
- time

<br>

\**Install scapy and a packet capture software (npcap ,pcap) before executing the script : 
pip install scapy*