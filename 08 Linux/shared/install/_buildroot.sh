#! /bin/sh
echo "# Klone Buildroot Git-Repository"

DEFAULT_RELEASE=2019.02

echo -n "Buildroot-Version [$DEFAULT_RELEASE] "
read RELEASE

if [ -z $RELEASE ]; then
    RELEASE=$DEFAULT_RELEASE
fi

git clone --branch $RELEASE.x --depth 1 git://git.buildroot.net/buildroot ~/buildroot
#wget -q -c http://buildroot.org/downloads/buildroot-#{RELEASE}.tar.gz
#tar axf buildroot-$RELEASE.tar.gz

mkdir -p ~/download
mkdir -p ~/make
mkdir -p ~/cache

echo ""
echo ""
echo ""

echo "Das war's. Jetzt in VirtualBox die Ordner \"shared\" und \"custom\""
echo "mit dem Host teilen, falls noch nicht geschehen. Anschließend die Maschine"
echo "neustarten und folgende Befehle für den ersten Build auszuführen:"
echo ""
echo "  $ cd ~/buildroot"
echo "  $ make O=../make BR2_EXTERNAL=../custom dhbw_minimal_defconfig"
echo "  $ cd ../make"
echo "  $ make BR2_JLEVEL=4"
echo ""

