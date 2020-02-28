#!/bin/sh

# Basierend auf der Vorlage des Projekts SDIM (IoT/Embedded-Workshop 2017)
# https://github.com/BoThomas/sdim.im
#
# Dieses Skript erzeugt ein RaspberryPi-Image mit debootstrap.
# Das Image enthält dann ein abgespecktes Raspbian-System und setzt sich
# dementsprechend aus vorkompilierten Paketen zusammen. Im Vergleich zu
# Buildroot lässt sich dadurch die Build-Zeit reduzieren, man hat aber
# dafür nicht so viele Freiheiten.

#
# Unterprogramme zur Anzeige von Meldungen
# Vgl. https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
#
print_title() {
	esc1=$(tput setaf 7)$(tput setab 4)$(tput bold)
	esc2=$(tput sgr0)
	up=$(tput cuu 1)$(tput cuf 2)

	echo
	echo -n "${esc1}╔════════════════════════════════════════════════════════════════════╗${esc2}"; echo
	echo -n "${esc1}║                                                                    ║${esc2}"; echo
	echo -n "${esc1}${up}$1${esc2}"; echo
	echo -n "${esc1}╚════════════════════════════════════════════════════════════════════╝${esc2}"; echo
	echo
}

print_error() {
	esc1=$(tput setaf 1)$(tput bold)$(tput bel)
	esc2=$(tput sgr0)
	echo "${esc1}🔥 [FEHLER]${esc2} $*"
}

print_warning() {
	esc1=$(tput setaf 3)$(tput bold)$(tput bel)
	esc2=$(tput sgr0)
	echo "${esc1}📣 [WARNUNG]${esc2} $*"
}

print_info() {
	esc1=$(tput setaf 4)$(tput bold)
	esc2=$(tput sgr0)
	echo "${esc1}🎶 [INFO]${esc2} $*"
}

#
# Unterprogramm zur Anzeige des Hilfetextes
#
show_help() {
	print_title "📜 Hilfe zu diesem Skript"

	print_info "$0                 - Baut das Image mit dem Konfigurationsverzeichnis debian"
	print_info "$0 <config_dir>    - Baut das Image mit dem Konfigurationsverzeichnis <config_dir>"
	print_info "$0 help            - Zeigt diesen Hilfetext"
	echo

	print_info "Wenn alles gut geht, befindet sich im Ausgabeverzeichnis ein Image namens sdcard.img."
	print_info "Dieses kann z.B. mit dd auf die SD-Karte des Raspberry Pi geschrieben werden."
	echo

	print_info "Die Ausgabe des Skripts wird in der Datei output.log protokolliert."
}

#
# Hauptprogramm
#
main() {
	##################################################################
	print_title "🛠️  Ermittelte Verzeichnise und Konfigurationsdateien"
	##################################################################

	# Startzeit und benutzte Verzeichnisse ausgeben
	print_info $(date)
	echo

	print_info "Arbeitsverzeichnis:           ${WORK_DIR}"
	print_info "Konfigurationsverzeichnis:    ${CONFIG_DIR}"
	print_info "Bootdateien:                  ${BOOT_DIR}"
	print_info "Overlayverzeichnis:           ${OVERLAY_DIR}"
	print_info "Ausgabeverzeichnis:           ${BUILD_DIR}"
	print_info "Neue Bootpartition:           ${BOOTFS_DIR}"
	print_info "Neue Wurzelpartition:         ${ROOTFS_DIR}"
	print_info "Debootstrap-Basissystem:      ${BASEFS_DIR}"
	echo

	# Konfiguration des neuen Images einlesen
	IMAGE_CONFIG="${CONFIG_DIR}/image.config"

	if [ -r "${IMAGE_CONFIG}" ]; then
		. ${IMAGE_CONFIG}
	else
		print_error "Konfigurationsdatei ${IMAGE_CONFIG} nicht gefunden"
		exit 1
	fi

	print_info "Image-Datei:                  ${IMAGE_FILE}"
	print_info "Image-Größe:                  ${IMAGE_SIZE} MiB"
	print_info "Boot-Größe:                   ${BOOT_SIZE} MiB"
	echo

        # Prüfen, ob alle benötigten Programmpakete vorhanden sind
        DISTRIBUTION=$(lsb_release -i | awk '{print $3}')
        DEPENDENCIES="qemu-user-static debootstrap kpartx psmisc dosfstools curl apt-transport-https"

        if [ "${DISTRIBUTION}" == "Ubuntu" ] || [ "${DISTRIBUTION}" == "Debian" ]; then
        	for package in $DEPENDENCIES; do
        		result=$(dpkg-query -W -f='${binary:Package}\n' $package 2>/dev/null | wc -l )
        		if [ ${result} -lt 1 ]; then
        			print_error "Benötigtes Paket $package wurde nicht gefunden. Bitte mit apt-get nachinstallieren."
        			exit 1
        		fi
        	done
        else
        	print_warning "Unbekannte Linux-Distribution ${DISTRIBUTION} erkannt."
        	print_warning "Stelle sicher, dass folgende Pakete installiert sind:"
        	print_warning "${DEPENDENCIES}"
        fi

	#################################################
	print_title "🛠️  Löschen der alten Arbeitsdateien"
	#################################################

	print_info "Fehler an dieser Stelle sind in der Regel unbedenklich."
	echo

	# Prozesse abschießen, die auf die Verzeichnisse zugreifen
	fuser -k ${IMAGE_FILE}
	fuser -k ${BOOTFS_DIR}
	fuser -k ${ROOTFS_DIR}

	# Partitionsmappings löschen und unmounten
	kpartx -d ${IMAGE_FILE}

	umount ${BOOTFS_DIR}

	umount ${ROOTFS_DIR}/_config
	umount ${ROOTFS_DIR}/boot
	umount ${ROOTFS_DIR}/proc
	umount ${ROOTFS_DIR}/sys
	umount ${ROOTFS_DIR}/dev
	umount ${ROOTFS_DIR}

	loop_devices=$(losetup -l -O NAME,BACK-FILE | grep ${IMAGE_FILE} | awk '/dev/ {print $1}')
	if [ "${loop_devices}" != "" ]; then
		for i in $(lsblk -l -p ${loop_devices} -o NAME,TYPE | awk '/part/ {print $1}'); do
			dmsetup remove ${i}
		done

		losetup -d ${loop_devices}
		kpartx -d ${IMAGE_FILE}
	fi

	# Altes Image und Dateisysteme löschen
	rm -rf ${IMAGE_FILE}
	rm -rf ${BOOTFS_DIR}
	rm -rf ${ROOTFS_DIR}

	case $1 in
		clean)
			rm -rf ${BUILD_DIR}
			return
			;;
	esac

	#################################################
	print_title "🛠️  Erzeugung des Dateisystem-Images"
	#################################################

	print_info "Erzeuge leeres Image mit Dateisystemen"

	# Leeres Image erzeugen
	dd if=/dev/zero of="${IMAGE_FILE}" bs=1M count=${IMAGE_SIZE}
	RC=$?

	if [ $RC -ne 0 ]; then
		print_error "DD wurde mit Return Code $RC beendet"
		exit 1
	fi

	# Partitionstabelle anlegen
	loop_device=$(losetup -f --show "${IMAGE_FILE}")

	cat <<-EOF | sfdisk --color=always ${loop_device}
		label: dos
		size=${BOOT_SIZE}MiB, type=0b, name=boot, bootable
		name=root
		EOF
	RC=$?

	if [ $RC -ne 0 ]; then
		print_error "SFDisk wurde mit Return Code $RC beendet. Dateisysteme konnte nicht erzeugt werden."
		exit 1
	fi

	losetup -d ${loop_device}

	# Dateisysteme innerhalb des Images anlegen
	boot_partition="$(kpartx -va "${IMAGE_FILE}" | awk '{print $3}' | head -1)"
	root_partition="$(kpartx -va "${IMAGE_FILE}" | awk '{print $3}' | tail -1)"
	sleep 2

	mkfs.vfat "/dev/mapper/${boot_partition}"
	mkfs.ext4 -F "/dev/mapper/${root_partition}"

	# Neue Dateisysteme mounten
	print_info "Mounte neue Dateisysteme für die Installation"

	mkdir -p ${BOOTFS_DIR}
	mkdir -p ${ROOTFS_DIR}

	mount /dev/mapper/${boot_partition} ${BOOTFS_DIR}
	RC=$?

	if [ $RC -ne 0 ]; then
		print_error "Mount wurde mit Return Code $RC beendet. Bootpartition konnte nicht gemountet werden."
		exit 1
	fi

	mount /dev/mapper/${root_partition} ${ROOTFS_DIR}
	RC=$?

	if [ $RC -ne 0 ]; then
		print_error "Mount wurde mit Return Code $RC beendet. Wurzelpartition konnte nicht gemountet werden."
		exit 1
	fi

	# Filesystem muss komplett leer sein, damit Debootstrap nicht abbricht
	rm -rf ${ROOTFS_DIR}/lost+found

	###############################################
	print_title "🛠️  Installation des Linux-Systems"
	###############################################

	print_info "Prüfe, ob ein vorheriger Debootstrap-Lauf wiederverwendet werden kann"

	if ls ${BASEFS_DIR}/*; then
		print_info "Okay, überspringe Debootstrap."
		SKIP_DEBOOTSTRAP=1
	else
		print_info "Schade. Dann geht es jetzt etwas länger."
		SKIP_DEBOOTSTRAP=0
	fi

	if [ $SKIP_DEBOOTSTRAP -eq 0 ]; then
		print_info "Starte Installation mit Debootstrap"

		mkdir -p ${BASEFS_DIR}

		export LANG=C
		export LANGUAGE=C
		export LC_ALL=C
		export DEBIAN_FRONTEND=noninteractive
		export DEBCONF_NONINTERACTIVE_SEEN=true

		mkdir -p ${CACHE_DIR}

		# Workaround um einen scheinbaren Bug in debootstrap. Die zusätzliche, über
		# base hinausgehenden Pakete, werden nicht sauber beim Leerzeichen getrennt
		# (sieht man mit --print-debs am Ende der Ausgabe), weshalb u.a. apt, apt-get
		# und apttitude (neben vielen anderen) nicht installiert werden. Dies wiederum
		# verhindert auch, dass die Datei /debootstrap/debootstrap angelegt wird.
		DEB_OPTIONS="${DEB_OPTIONS} --include=apt,aptitude"

	        DBS_VERSION=`debootstrap --version | cut -d " " -f2`
	        USE_CACHE_DIR=""

	        if dpkg --compare-versions ${DBS_VERSION} ge 1.0.112; then
        		USE_CACHE_DIR="--cache_dir=${CACHE_DIR}"
	        fi

		# Endet immer mit RC 1, auch bei Erfolg ?!?
#		debootstrap --arch=armhf --foreign --no-check-gpg --variant=minbase ${USE_CACHE_DIR} ${DEB_OPTIONS} ${DEB_VERSION} ${BASEFS_DIR} ${DEB_MIRROR}
		debootstrap --arch=armhf --foreign --no-check-gpg ${USE_CACHE_DIR} ${DEB_OPTIONS} ${DEB_VERSION} ${BASEFS_DIR} ${DEB_MIRROR}
		RC=$?

		if [ $RC -ne 0 ]; then
			echo
			tail -n 5 ${BASEFS_DIR}/debootstrap/debootstrap.log
			echo

			print_warning "Debootstrap wurde mit Return Code $RC beendet."
			echo
		fi
	fi

	print_info "Kopiere Basissystem in das Image"

	cp -av ${BASEFS_DIR}/* ${ROOTFS_DIR}

	print_info "Starte zweite Phase von Debootstrap im neuen System"

	cp /usr/bin/qemu-arm-static ${ROOTFS_DIR}/usr/bin

	# Endet immer mit RC 1, auch bei Erfolg ?!?
	chroot ${ROOTFS_DIR} /debootstrap/debootstrap --second-stage
	RC=$?

	if [ $RC -ne 0 ]; then
		echo
		tail -n 5 ${ROOTFS_DIR}/debootstrap/debootstrap.log
		echo

		print_warning "Debootstrap wurde mit Return Code $RC beendet."
		echo
	fi

	print_info "Kopiere /etc/apt vorab für die Installation der Zusatzpakete"

	if [ -d ${OVERLAY_DIR}/etc/apt ]; then
		cp -rv ${OVERLAY_DIR}/etc/apt/* ${ROOTFS_DIR}/etc/apt
	fi

	print_info "Installiere ausgewählte Zusatzpakete: ${PACKAGES}"

	mkdir -p ${ROOTFS_DIR}/boot
	mkdir -p ${ROOTFS_DIR}/proc
	mkdir -p ${ROOTFS_DIR}/sys
	mkdir -p ${ROOTFS_DIR}/dev

	mount -o bind ${BOOTFS_DIR} ${ROOTFS_DIR}/boot
	mount -t proc proc ${ROOTFS_DIR}/proc
	mount -t sysfs sysfs ${ROOTFS_DIR}/sys
	mount -o bind /dev ${ROOTFS_DIR}/dev

	chroot ${ROOTFS_DIR} /usr/bin/apt-get -q update
	chroot ${ROOTFS_DIR} /usr/bin/apt-get -q -y --no-install-recommends dist-upgrade
	chroot ${ROOTFS_DIR} /usr/bin/apt-get -q -y --no-install-recommends install ${PACKAGES}
	RC=$?

	if [ $RC -ne 0 ]; then
		print_error "Apt-Get wurde mit Return Code $RC beendet. Die Zusatzpakete konnten nicht vollständig installiert werden."
		exit 1
	fi

	print_info "Kopiere Inhalt des Overlayverzeichnisses"
	cp -rv ${OVERLAY_DIR}/* ${ROOTFS_DIR}

	if [ -f ${CONFIG_DIR}/modify-rootfs.sh ]; then
		print_info "Starte Skript zur weiteren Anpassung des Dateisystems"
		cp ${CONFIG_DIR}/modify-rootfs.sh ${ROOTFS_DIR}
		chmod +x ${ROOTFS_DIR}/modify-rootfs.sh

		mkdir -p ${ROOTFS_DIR}/_config
		mount -o bind,ro ${CONFIG_DIR} ${ROOTFS_DIR}/_config

		chroot ${ROOTFS_DIR} /modify-rootfs.sh
		RC=$?

		if [ $RC -ne 0 ]; then
			print_error "Das Skript zur Anpassung des Dateisystems wurde mit Return Code $RC beendet. Es fehlen möglicherweise einige Anpassungen."
			exit 1
		fi

		rm ${ROOTFS_DIR}/modify-rootfs.sh
		umount ${ROOTFS_DIR}/_config
		rm ${ROOTFS_DIR}/_config
	fi

	print_info "Starte Aufräumarbeiten im neuen System"
	chroot ${ROOTFS_DIR} /usr/bin/apt-get -q -y autoremove
	chroot ${ROOTFS_DIR} /usr/bin/apt-get -q clean

	chroot ${ROOTFS_DIR} rm /usr/bin/qemu-arm-static

	########################################
	print_title "🛠️  Update der Boot-Dateien"
	########################################

#	print_info "Der Kernel wird später durch das Grundsystem installiert"
	cp -rv ${BOOT_DIR}/* ${BOOTFS_DIR}

	######################################
	print_title "🏁 Vorgang abgeschlossen"
	######################################

	# Dateisysteme aushängen
	print_info "Hänge temporäre Dateisysteme wieder aus"

	fuser -k ${BOOTFS_DIR}
	umount ${BOOTFS_DIR}

	fuser -k ${ROOTFS_DIR}
	umount ${ROOTFS_DIR}/boot
	umount ${ROOTFS_DIR}/proc
	umount ${ROOTFS_DIR}/sys
	umount ${ROOTFS_DIR}/dev
	umount ${ROOTFS_DIR}

	kpartx -d ${IMAGE_FILE}

	# Efolgsmeldung ausgeben
	print_info "Erzeugtes Image: $(ls -alh ${IMAGE_FILE})"
	print_info "Du kannst das Image nun auf eine SD-Karte übertragen. Viel Spaß damit!"
	print_info $(date)
}

#
# Skript als Root ausführen und Ausgabe protokollieren
#
if [ "$1" = "help" ]; then
	show_help
elif [ "$1" = "__main__" ]; then
	shift
	main $@
else
	# Benötigte Verzeichnispfade ermitteln.
	# Wird hier gemacht, damit das Logfile im richtigen Verzeichnis angelegt wird.
	export WORK_DIR=$(dirname "$0")
	export WORK_DIR=$(cd "$WORK_DIR" && pwd )

	if [ "$1" = "" -o "$1" = "clean" ]; then
		NAME="debian"
	else
		NAME="$1"
	fi

	export CONFIG_DIR=${WORK_DIR}/${NAME}
	export BOOT_DIR=${CONFIG_DIR}/boot
	export OVERLAY_DIR=${CONFIG_DIR}/overlay
	export CACHE_DIR=${WORK_DIR}/out/_cache
	export BUILD_DIR=${WORK_DIR}/out/${NAME}
	export BOOTFS_DIR=${BUILD_DIR}/boot
	export ROOTFS_DIR=${BUILD_DIR}/root
	export BASEFS_DIR=${BUILD_DIR}/base

	# Skript als Root erneut starten
	mkdir -p ${BUILD_DIR}
	#sudo --preserve-env=WORK_DIR,CONFIG_DIR,BOOT_DIR,OVERLAY_DIR,CACHE_DIR,BUILD_DIR,BOOTFS_DIR,ROOTFS_DIR,BASEFS_DIR bash $0 "__main__" $@ 2>&1 | tee ${BUILD_DIR}/output.log
	SUDO="sudo WORK_DIR=$WORK_DIR CONFIG_DIR=$CONFIG_DIR BOOT_DIR=$BOOT_DIR OVERLAY_DIR=$OVERLAY_DIR CACHE_DIR=$CACHE_DIR BUILD_DIR=$BUILD_DIR BOOTFS_DIR=$BOOTFS_DIR ROOTFS_DIR=$ROOTFS_DIR BASEFS_DIR=$BASEFS_DIR"
	$SUDO bash $0 "__main__" $@ 2>&1 | tee ${BUILD_DIR}/output.log
fi

echo
