UPDATE=sudo apt-get update -y
INSTALL=sudo apt-get install -y

all: fping python_scapy


fping:
	$(INSTALL) fping

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