#! /bin/sh
echo ">> Füge weitere Bootparameter in der cmdline.txt hinzu"

# Einlesen der Bootparameter aus cmdline.txt
CMDLINE_TXT="$BINARIES_DIR/rpi-firmware/cmdline.txt"

grep "quiet" "$CMDLINE_TXT"
if [ $? -eq 0 ]; then exit 0; fi

BOOT_PARAMS=""

while read line; do
    if [ -z "$BOOT_PARAMS" ]; then
        BOOT_PARAMS="$line"
    else
        BOOT_PARAMS="$BOOT_PARAMS $line"
    fi
done < "$CMDLINE_TXT"

# Fügen Sie hier nach Bedarf weitere Parameter hinzu
BOOT_PARAMS="$BOOT_PARAMS quiet"

# Veränderten Inhalt in cmdline.txt schreiben
echo "$BOOT_PARAMS" > "$CMDLINE_TXT"
