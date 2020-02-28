#! /bin/bash
# Diese Datei wird via CHROOT im neuen System ausgeführt, um weitere
# Pakete zu installieren, und das System zu konfigurieren.

set -e


########################################
echo "----- Generiere Locales neu -----"
########################################
locale-gen



############################################
echo "----- Füge Login-Benutzer hinzu -----"
############################################
useradd --no-create-home --shell /bin/bash mulder
echo "mulder:xfiles" | chpasswd
adduser mulder sudo
mkdir /home/mulder
chown -R mulder:mulder /home/mulder

useradd --no-create-home --shell /bin/bash scully
echo "scully:xfiles" | chpasswd
adduser scully sudo
mkdir /home/scully
chown -R scully:scully /home/scully



##########################################
echo "----- Deaktiviere Root-Zugang -----"
##########################################
usermod --expiredate 1 root



######################################################
echo "----- Aktiviere zusätzliche Systemdienste -----"
######################################################
systemctl enable my-keyboard-layout
systemctl enable my-allow-framebuffer
#systemctl enable my-regenerate-ssh-keys



## Kommentieren Sie die folgenden Zeilen ein, um den interaktiven Login
## auf der Konsole zu verhindern. Stattdessen müssen Sie dann natürlich
## sicherstellen, dass irgend ein anderes Programm stattdessen gestartet
## wird. Wie das geht, steht im Skript. :-)
#echo "----- Deaktiviere interaktiven Shell-Login -----"
#systemctl disable getty@


## Kommentieren Sie die folgenden Zeilen ein, wenn Sie sich von der Seite
## https://www.bell-sw.com/java.html eine Java-Laufzeitumgebung heruntergeladen
## haben und diese nun in das Image integrieren möchten. Den Dateinamen beim
## tar-Befehl müssen Sie dann natürlich noch anpassen.
#echo "----- Entpacke Java-Laufzeitumgebung ----"
#PWD=$(pwd)
#cd /opt
#tar -xvzf /_config/bellsoft-jdk12.0.1-linux-arm32-vfp-hflt-lite.tar.gz
#mv jdk* jdk
#cd $PWD


## Kommentieren Sie die folgenden Zeilen ein, um WiringPi zu installieren.
## Sie benötigen es, wenn Sie z.B. mit Pi4J aus Java heraus auf die GPIO-Pins
## zugreifen oder den gpio-Konsolenbefehl nutzen wollen. Leider ist WiringPi
## Stand Mai 2019 noch nicht in Raspbian-Stable enthalten, so dass wir es gemäß
## Anleitung von http://wiringpi.com/download-and-install/ nachinstallieren
## hier müssen.
#wget --no-check-certificate https://lion.drogon.net/wiringpi-2.50-1.deb
#dpkg -i wiringpi-2.50-1.deb
#rm wiringpi-2.50-1.deb
