#! /bin/sh
echo "# Installiere Debootstrap-Skripte"

# Konflikt: qemu-user-binfmt
sudo apt-get -q -y --no-install-recommends install qemu qemu-user-static binfmt-support
# Überprüfung mit sudo update-binfmts --display

sudo apt-get -q -y --no-install-recommends install git kpartx psmisc dosfstools curl
sudo apt-get -q -y --no-install-recommends install debootstrap

cp ../debootstrap/db-build.sh ~
chmod +x ~/db-build.sh

mkdir -p ~/out
