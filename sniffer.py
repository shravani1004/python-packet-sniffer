from scapy.all import *
from data_store import add_packet
from vt_check import check_ip
import threading
import time

seen = set()

def process_packet(packet):

    if packet.haslayer(IP):

        src = packet[IP].src
        dst = packet[IP].dst

        if dst not in seen:
            seen.add(dst)

            status = check_ip(dst)

            add_packet({
                "src": src,
                "dst": dst,
                "status": status
            })

            print(f"{src} → {dst} | {status}")

def start_sniffing():
    sniff(prn=process_packet, store=0)

def run_sniffer():
    t = threading.Thread(target=start_sniffing)
    t.daemon = True
    t.start()