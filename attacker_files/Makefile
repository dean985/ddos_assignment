INSTALL=sudo apt install

python_lib:
	$(INSTALL) python-scapy
	$(INSTALL) python3-scapy

c_ddos: ddos.c
	rm syns_results_c.txt
	gcc -g ddos.c -o syn_flood
