#! /bin/sh
set +e
pwd=`realpath $(dirname $0)`

JDK_ARCHIV=ejdk-*-linux-arm*.tar.gz
OVERLAY_DIR_JAVA=board/rootfs_overlay_java
OVERLAY_DIR_CUSTOM=board/rootfs_overlay
JFX_URL="http://gluonhq.com/download/javafx-embedded-sdk/"

echo_red () {
    echo "\033[31m$1\033[0m"
}

echo_green () {
    echo "\033[32m$1\033[0m"
}

echo_yellow () {
    echo "\033[33m$1\033[0m"
}

delete_file () {
    FILENAME=$1
    SHORTNAME=${FILENAME#$pwd/$OVERLAY_DIR_JAVA/}
    echo -n "  » Lösche $SHORTNAME: "

    if [ ! -r $FILENAME ]; then
        echo_yellow "NICHT GEFUNDEN"
    else
        SIZE=`du --summarize -h $FILENAME`
        set -f
        set $SIZE
        SIZE=$1
        set +f

        rm -rf $FILENAME
        echo_green "$SIZE"
    fi
}

echo ""
echo "==============================================="
echo "Filesystem Overlay mit Java Runtime vorbereiten"
echo "==============================================="
echo ""
echo "Dieses Skript hilft Ihnen, das Oracle JDK zu entpacken, um die Java Runtime"
echo "und JavaFX in die Firmware aufnehmen zu können."
echo ""

# JDK-Archiv suchen
echo -n "  » Suche Datei ejdk-*-linux-arm*.tar.gz: "

if [ ! -r $pwd/$JDK_ARCHIV ]; then
    echo_red "NICHT GEFUNDEN!"
    echo_yellow ""
    echo_yellow "  Besuchen Sie die Oracle-Webseite und laden Sie das aktuelle"
    echo_yellow "  \"Java SE Embedded\" für \"ARM v6/v7 Linux - VFP, HardFP ABI,"
    echo_yellow "  Little Endian\" herunter. Legen Sie das Archiv hier in diesem"
    echo_yellow "  diesem Verzeichnis ab: $pwd"
    echo_yellow ""
    exit 1
else
    echo_green "OK"
fi

#  Overlay-Verzeichnis löschen und neu anlegen
echo -n "  » Lösche Overlay-Verzeichnis $OVERLAY_DIR_JAVA: "

if [ ! -r $pwd/$OVERLAY_DIR_JAVA ]; then
    echo_yellow "NICHT GEFUNDEN"
else
    rm -rf $pwd/$OVERLAY_DIR_JAVA
    echo_green "OK"
fi

# Archiv entpacken
echo -n "  » Entpacke Archiv $JDK_ARCHIV: "
mkdir -p $pwd/$OVERLAY_DIR_JAVA
tar -xa -C $pwd/$OVERLAY_DIR_JAVA -f $pwd/$JDK_ARCHIV 2> /dev/null
RC=$?

if [ $RC -ne 0 ]; then
    echo_red "FEHLER CODE $RC!"
    echo_yellow ""
    echo_yellow "  Das Archiv konnte nicht entpackt werden. Bitte prüfen Sie, ob Sie"
    echo_yellow "  die richtige Datei heruntergeladen haben."
    echo_yellow ""
    echo_yellow "  Momentan hat die Datei folgenden Dateityp:"
    echo_yellow ""
    file $pwd/$JDK_ARCHIV
    echo_yellow ""
    exit 1
else
    echo_green "OK"
fi

# Java Runtime nach /opt/java verschieben, den Rest löschen
echo -n "  » Verschiebe Java Runtime nach /opt/java: "
mkdir -p $pwd/$OVERLAY_DIR_JAVA/opt
mv $pwd/$OVERLAY_DIR_JAVA/ejdk*/linux*/jre $pwd/$OVERLAY_DIR_JAVA/opt/java
echo_green "OK"

delete_file $pwd/$OVERLAY_DIR_JAVA/ejdk*
delete_file $pwd/$OVERLAY_DIR_JAVA/opt/java/COPYRIGHT
delete_file $pwd/$OVERLAY_DIR_JAVA/opt/java/README
delete_file $pwd/$OVERLAY_DIR_JAVA/opt/java/release
delete_file $pwd/$OVERLAY_DIR_JAVA/opt/java/THIRDPARTYLICENSEREADME.txt

# JavaFX herunterladen und installieren
if [ ! -f javafx.zip ]; then
    echo -n "  » Lade JavaFX herunter: "
    wget -O javafx.zip $JFX_URL > /dev/null 2> /dev/null
    RC=$?

    if [ $RC -ne 0 ]; then
        rm -rf javafx.zip

        echo_red "FEHLER CODE $RC!"
        echo_yellow ""
        echo_yellow "  JavaFX konnte nicht heruntergeladen werden. Bitte prüfen Sie die"
        echo_yellow "  Download-URL und passen Sie am Anfang dieses Skripts die Variable"
        echo_yellow "  JFX_URL entsprechend an:"
        echo_yellow ""
        echo_yellow "  $JFX_URL"
        echo_yellow ""
        echo_yellow "  HINWEIS: Seit Java 8u33 liefert Oracle JavaFX nicht mehr als Teil"
        echo_yellow "  von Java für ARM-Prozessoren aus. Im OpenJFX-Projekt wird es aber"
        echo_yellow "  weiterentwickelt. Da das Cross-Compiling sehr aufwändig ist, wird"
        echo_yellow "  hier versucht, eine vorkompilierte Version herunterzuladen."
        exit 1
    else
        echo_green "OK"
    fi
fi

echo -n "  » Entpacke JavaFX: "
unzip javafx.zip -d $pwd/$OVERLAY_DIR_JAVA > /dev/null 2> /dev/null

if [ $RC -ne 0 ]; then
    rm -rf javafx.zip

    echo_red "FEHLER CODE $RC!"
    exit 1
else
    echo_green "OK"
fi

cp -fr $pwd/$OVERLAY_DIR_JAVA/arm*sdk/rt/lib/* $pwd/$OVERLAY_DIR_JAVA/opt/java/lib
delete_file $pwd/$OVERLAY_DIR_JAVA/arm*sdk

# /opt/java/bin dem PATH hinzufügen
echo -n "  » Erweitere PATH um /opt/java/bin: "

mkdir -p $pwd/$OVERLAY_DIR_JAVA/etc/profile.d
echo "export PATH=\$PATH:/opt/java/bin" > $pwd/$OVERLAY_DIR_JAVA/etc/profile.d/java.sh

if [ $RC -ne 0 ]; then
    echo_red "FEHLER CODE $RC!"
    exit 1
else
    echo_green "OK"
fi

chmod +x $pwd/$OVERLAY_DIR_JAVA/etc/profile.d/java.sh

# Das war's!
echo_yellow ""
echo_yellow "Fertig! Starten Sie nun die Buildroot-Konfiguration mit \"make menuconfig\""
echo_yellow "und nehmen Sie folgende Einstellung vor, um die Java Runtime in die Firmware"
echo_yellow "zu integrieren:"
echo_yellow ""
echo_yellow "  System Configuration"
echo_yellow "    ⤷ Root filesystem overlay directories:"
echo_yellow "       ⤷ Fügen Sie folgenden Eintrag hinzu:"
echo_yellow "         \033[33;1m\$(BR2_EXTERNAL_DHBW_PATH)/$OVERLAY_DIR_JAVA"
echo_yellow ""
echo_yellow "TIPP: Sie können das Verzeichnis \033[33;1m$OVERLAY_DIR_CUSTOM"
echo_yellow "nutzen, um eigene Dateien in die Firmware aufzunehmen. Legen Sie dort"
echo_yellow "z.B. ein Verzeichnis /opt/dhbw für Ihre kompilierten Java-Dateien an."
echo_yellow ""
