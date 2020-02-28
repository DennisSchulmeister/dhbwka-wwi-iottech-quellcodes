#! /bin/sh
echo "# Installiere pi-gen"

sudo apt-get -q -y --no-install-recommends install coreutils quilt parted qemu-user-static debootstrap zerofree zip dosfstools bsdtar libcap2-bin grep rsync xz-utils file git curl bc
git clone https://github.com/RPi-Distro/pi-gen.git ~/pi-gen
