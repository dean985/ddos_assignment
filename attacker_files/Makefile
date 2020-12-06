INSTALL=sudo apt install -y
UPDATE=sudo apt update

python_lib:
	$(UPDATE)
	$(INSTALL) software-properties-common -y
	sudo add-apt-repository ppa:deadsnakes/ppa -y
	$(UPDATE)
	$(INSTALL) python3.8 -y
	$(INSTALL) python3.8-distutils -y
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
	python3.8 get-pip.py
	$(INSTALL) python-scapy
	$(INSTALL) python3-scapy

c_ddos: ddos.c
	rm -f syns_results_c.txt
	gcc -g ddos.c -o syn_flood
