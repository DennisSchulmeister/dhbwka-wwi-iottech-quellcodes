#! /bin/sh

# Installationsskript des LED-Laufschrift-Beispiels
# Das Skript kopiert den Quellcode nach /opt/ledmsgbar,
# installiert alle benötigten Debian-Pakete, legt ein
# Python-Environment an, in das alle benötigten Python-
# Module installiert werden und erzeugt eine SystemD
# Unit zum automatischen Start beim Hochfahren des Pi.

INSTALL_DIR=/opt/ledmsgbar

echo "========================"
echo "ledmsgbar - Installation"
echo "========================"
echo


echo
echo ">>> Lösche vorherige Installation"
echo
sudo rm -r $INSTALL_DIR


echo
echo ">>> Kopiere Programm nach $INSTALL_DIR"
echo

sudo mkdir -p $INSTALL_DIR
sudo cp -r * $INSTALL_DIR


echo
echo ">>> Installiere benötigte Pakete und Python-Module"
echo

sudo usermod -a -G spi,gpio $USER
sudo apt install -y build-essential python3-dev python3-pip python3-venv libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5

sudo python3 -m venv "$INSTALL_DIR/env"
sudo "$INSTALL_DIR"/env/bin/pip3 install -r requirements.txt


echo
echo ">>> Erzeuge SystemD Service zum Automatischen Start das Programms"
echo


sed -e "s!#INSTALL_DIR#!$INSTALL_DIR!g" ledmsgbar.service > /tmp/ledmsgbar.service
sudo cp /tmp/ledmsgbar.service /etc/systemd/system
rm /tmp/ledmsgbar.service

sudo systemctl daemon-reload
sudo systemctl enable ledmsgbar
sudo systemctl start ledmsgbar
