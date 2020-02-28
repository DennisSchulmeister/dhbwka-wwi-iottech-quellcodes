#! /bin/sh
sudo dd if=sdcard.img of=/dev/mmcblk0 status=progress
sudo sync
