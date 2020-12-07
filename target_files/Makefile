# Intended to be used only for the purpuse of installing an apache server

INSTALL=sudo apt install -y
UPDATE=sudo apt-get update -y

all:
	$(UPDATE)
	$(INSTALL) apache2
	sudo ufw allow 'Apache'
	sudo ufw status
	sudo systemctl restart apache2.service
	echo "Your apache server IP: ' 
	hostname -I | awk '{print $1}'