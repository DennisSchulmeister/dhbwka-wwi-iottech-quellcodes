#! /bin/sh

# Installationsskript der Beispiele zum Ansteuern verschiedener Bauteile.
# Das Skript legt in ./env in Python-Environment an und installiert darin
# alle externen Python-Module. Davor werden noch ein paar Debian-Pakete
# installiert.

ENV_DIR=./env

echo "======================="
echo "bauteile - Installation"
echo "======================="
echo


echo
echo ">>> Lösche vorherigs Environment"
echo
sudo rm -r $ENV_DIR

echo
echo ">>> Installiere benötigte Pakete"
echo

sudo usermod -a -G spi,gpio $USER
sudo apt install -y build-essential python3-dev python3-pip python3-venv python3-numpy i2c_tools

echo
echo ">>> Installiere Python-Module"
echo
sudo python3 -m venv --system-site-packages $ENV_DIR
sudo $ENV_DIR/bin/pip3 install -r requirements.txt
