INSTALL=sudo apt install

python_lib:
	$(INSTALL) python-scapy
	$(INSTALL) python3-scapy

c_ddos: ddos.c
	gcc -o ddos ddos.c -lpthread