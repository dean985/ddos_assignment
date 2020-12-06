INSTALL=sudo apt install -y
UPDATE=sudo apt update

python_setup:
	$(UPDATE)
	$(INSTALL) software-properties-common -y
	sudo add-apt-repository ppa:deadsnakes/ppa -y
	$(UPDATE)
	$(INSTALL) python3.8 -y
	$(INSTALL) python3.8-distutils -y
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
	python3.8 get-pip.py
	$(INSTALL) python-scapy
	pip3.8 install scapy

c_ddos: ddos.c
	rm -f syns_results_c.txt
	gcc -g ddos.c -o syn_flood

p_ddos: ddos.py
	rm -f syns_results_c.txt
	sudo python3.8 ddos.py 10.0.2.5 80 100
