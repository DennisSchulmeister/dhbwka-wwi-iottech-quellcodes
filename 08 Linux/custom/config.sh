#! /bin/sh
echo ">> Nehme Änderungen an der config.txt vor"
CONFIG_TXT="$BINARIES_DIR/rpi-firmware/config.txt"

grep "dtoverlay=vc4-fkms-v3d" "$CONFIG_TXT"
if [ $? -eq 0 ]; then exit 0; fi

sed -i -e 's/gpu_mem_256=100/gpu_mem_256=128/g' "$CONFIG_TXT"
sed -i -e 's/gpu_mem_512=100/gpu_mem_512=128/g' "$CONFIG_TXT"
sed -i -e 's/gpu_mem_1024=100/gpu_mem_1024=128/g' "$CONFIG_TXT"

cat <<EOF >> "$CONFIG_TXT"

# Aktivieren der 3D-Beschleunigung. Damit man etwas sieht, muss beim Hochfahren
# das Kernelmodul vc4 geladen werden. Sollte eigentlich automatisch passieren,
# das scheint aber nicht immer zu klappen. Deshalb muss in der /etc/inittab
# zur Sicherheit der Befehl "modprobe -a vc4" ausgeführt werden, damit man
# was auf dem Bildschirm sieht
dtoverlay=vc4-fkms-v3d

# Bild auf dem RaspberryPi-Touch-Display drehen
# Vgl. https://maker-tutorials.com/raspberry-pi-touchscreen-installieren-und-anschliessen-tipps-tricks/
#
# lcd_rotate=0          ->    Normal
# lcd_rotate=1          ->    90 Grad
# lcd_rotate=2          ->    180 Grad
# lcd_rotate=3          ->    270 Grad
# lcd_rotate=0x10000    ->    horizontal spiegeln
# lcd_rotate=0x20000    ->    vertikal spiegeln
lcd_rotate=2
EOF
