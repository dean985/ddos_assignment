UPDATE=sudo apt-get update -y
INSTALL=sudo apt-get install -y

all: hping python_scapy


hping:
	$(INSTALL) hping3

python_scapy:
	$(UPDATE)
	$(INSTALL) software-properties-common 
	sudo add-apt-repository ppa:deadsnakes/ppa 
	$(UPDATE)
	$(INSTALL) python3.8 
	$(INSTALL) python3.8-distutils 
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
	python3.8 get-pip.py
	pip3.8 install scapy



start_c:
	sudo hping3 10.0.2.12 -V -S -p 80 > pings_results_c_raw.txt

start_py:
	sudo hping3 10.0.2.12 -V -S -p 80 > pings_results_p_raw.txt
