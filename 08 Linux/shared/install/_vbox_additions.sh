#! /bin/sh
echo "# Bereite Installation der VirtualBox Guest Additions vor"

sudo apt-get -q -y --no-install-recommends install linux-headers-amd64 virtualbox-guest-dkms virtualbox-guest-utils

echo ""
echo ""
echo "Befehl zum Neubauen der VBox-Header: sudo dpkg-reconfigure virtualbox-guest-dkms"

#sudo apt-get -q -y install module-assistant
#sudo m-a prepare
#
#echo ""
#echo ""
#echo "Nun in VirtualBox auf \"Devices\" --> \"Insert Guest Additions\" klicken."
#echo "Anschließend ENTER um fortzufahren"
#read dummy
#
#sudo mount /media/cdrom
#sudo mkdir -p /etc/depmod.d
#sudo sh /media/cdrom/VBoxLinuxAdditions.run
#sudo umount /media/cdrom
#
#echo ""
#echo ""
#echo "Die CD mit den Guest Additions kann nun in VirtualBox ausgeworfen werden."
#echo "Anschließend ENTER um fortzufahren"
#read dummy
