#! /bin/sh
# ============================================================================
# Hilfsskript zur Installation der benötigten Pakete in einer leeren Debian VM
# ============================================================================

# Benutzer: buildroot       (Arbeitsuser)
# Passwort: debian

# Benutzer: root            (Superuser)
# Passwort: debian

# Benötigte Pakete
echo "# Aktiviere Stable und Testing-Repositories"

. /etc/os-release
DEBIAN_NAME=`echo $VERSION | cut -d "(" -f2 | cut -d ")" -f1`
SUDO="sudo DEBIAN_NAME=$DEBIAN_NAME"

sudo rm /etc/apt/sources.list
$SUDO sh -c 'echo "deb http://ftp.de.debian.org/debian/ $DEBIAN_NAME main contrib non-free" >> /etc/apt/sources.list'
$SUDO sh -c 'echo "deb http://security.debian.org/ $DEBIAN_NAME/updates main contrib non-free" >> /etc/apt/sources.list'
$SUDO sh -c 'echo "deb http://ftp.de.debian.org/debian/ $DEBIAN_NAME-updates main contrib non-free" >> /etc/apt/sources.list'
$SUDO sh -c 'echo "deb http://ftp.de.debian.org/debian/ $DEBIAN_NAME-backports main contrib non-free" >> /etc/apt/sources.list'
#$SUDO sh -c 'echo "deb http://ftp.de.debian.org/debian/ testing main" >> /etc/apt/sources.list'
#$SUDO sh -c 'echo "deb http://security.debian.org/ testing/updates main" >> /etc/apt/sources.list'

echo ""
echo ""
echo ""
echo "# Grundinstallation der benötigten Linux-Pakete"

sudo apt-get -q update
sudo apt-get -q -y --no-install-recommends dist-upgrade
sudo apt-get -q -y --no-install-recommends install aptitude apt-transport-https locales-all gpm
sudo apt-get -q -y --no-install-recommends install build-essential libncurses5-dev git bzr cvs mercurial subversion libc6 unzip zip gawk pkg-config autoconf libtool python-setuptools python3-setuptools cmake
sudo apt-get -q -y --no-install-recommends install rsync bc byobu
byobu-enable
byobu-prompt
sudo cp ./nanorc /etc

##sudo apt-get -q -y openjdk-7-jdk libX11-dev libxext-dev libxrender-dev libxtst-dev libxt-dev libcups2-dev libfreetype6-dev libxinerama-dev libxcomposite-dev libasound2-dev
##sudo ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/lib/jvm/openjdk
#sudo apt-get -q -y install default-jdk

sudo apt-get -q -y autoremove
sudo apt-get -q -y clean

## VirtualBox-Additions und Geteilte Verzeichnisse
echo ""
echo ""
echo ""
./_vbox_additions.sh
./_mount_dirs.sh

# Farbiger Prompt
echo ""
echo ""
echo ""
echo "# Konfiguriere farbigen Prompt"

sudo rm -f /etc/profile.d/des-prompt.sh
sudo sh -c 'echo "# DES Tue May 13, 2014: Custom prompt" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "# blue (1;34m): workstations" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "# red (1;31m): physical servers, vm hosts" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "# green (1;32m): virtual servers, vm guests" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "# yellow (1;33m): docker container" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "if [ \"$PS1\" ]; then" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "    color1=\"\[\\033[1;31m\]\"" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "    color2=\"\[\\033[0m\]\"" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "    PS1=\"\${color1}\u@\h\${color2}:\w\$ \"" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "    unset color1 color2" >> /etc/profile.d/des-prompt.sh'
sudo sh -c 'echo "fi" >> /etc/profile.d/des-prompt.sh'

# Buildroot
echo ""
echo ""
echo ""
./_buildroot.sh

# Multistrap
echo ""
echo ""
echo ""
./_debootstrap.sh

# pi-gen
echo ""
echo ""
echo ""
./_pi-gen.sh
