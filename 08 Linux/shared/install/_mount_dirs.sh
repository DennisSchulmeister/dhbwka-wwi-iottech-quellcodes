#! /bin/sh
echo "# Erlaube poweroff, mount & Co. via sudo"

sudo rm -f /etc/sudoers.d/des-poweroff
sudo sh -c 'echo "Cmnd_Alias SHUTDOWN_CMDS = /sbin/shutdown, /sbin/halt, /sbin/reboot, /sbin/poweroff" >> /etc/sudoers.d/des-poweroff'
sudo sh -c 'echo "ALL ALL=(ALL) NOPASSWD: SHUTDOWN_CMDS" >> /etc/sudoers.d/des-poweroff'

sudo rm -f /etc/sudoers.d/des-mount
sudo sh -c 'echo "Cmnd_Alias MOUNT_CMDS = /bin/mount, /bin/umount" >> /etc/sudoers.d/des-mount'
sudo sh -c 'echo "ALL ALL=(ALL) NOPASSWD: MOUNT_CMDS" >> /etc/sudoers.d/des-mount'

echo ""
echo ""
echo "# Lege benutzerspezifische systemd-Services an"

mkdir -p ~/custom
mkdir -p ~/shared
mkdir -p ~/debian

mkdir -p ~/.config/systemd/user
rm -f ~/.config/systemd/user/mount-vbox.service
echo "[Unit]"                                                                              >> ~/.config/systemd/user/mount-vbox.service
echo "Description=Mount Shared VirtualBox Directories"                                     >> ~/.config/systemd/user/mount-vbox.service
echo ""                                                                                    >> ~/.config/systemd/user/mount-vbox.service
echo "[Service]"                                                                           >> ~/.config/systemd/user/mount-vbox.service
echo "Type=oneshot"                                                                        >> ~/.config/systemd/user/mount-vbox.service
echo "ExecStart=/usr/bin/sudo mount -t vboxsf -o rw,uid=1000,gid=1000 custom $HOME/custom" >> ~/.config/systemd/user/mount-vbox.service
echo "ExecStart=/usr/bin/sudo mount -t vboxsf -o rw,uid=1000,gid=1000 shared $HOME/shared" >> ~/.config/systemd/user/mount-vbox.service
echo "ExecStart=/usr/bin/sudo mount -t vboxsf -o rw,uid=1000,gid=1000 debian $HOME/debian" >> ~/.config/systemd/user/mount-vbox.service
echo ""                                                                                    >> ~/.config/systemd/user/mount-vbox.service
echo "[Install]"                                                                           >> ~/.config/systemd/user/mount-vbox.service
echo "WantedBy=default.target"                                                             >> ~/.config/systemd/user/mount-vbox.service

systemctl --user enable mount-vbox
systemctl --user start mount-vbox

echo ""
echo ""
echo "Status der Mounts anzeigen: systemctl --user status mount-vbox"
echo ""
systemctl --user status mount-vbox

#sudo mount -t vboxsf -o rw,uid=1000,gid=1000 custom $HOME/custom
#sudo mount -t vboxsf -o rw,uid=1000,gid=1000 shared $HOME/shared
#sudo mount -t vboxsf -o rw,uid=1000,gid=1000 debian $HOME/debian
#
#sudo sh -c 'echo "#!/bin/sh -e" > /etc/rc.local'
#sudo sh -c 'echo "mount -t vboxsf -o rw,uid=1000,gid=1000 custom $HOME/custom" >> /etc/rc.local'
#sudo sh -c 'echo "mount -t vboxsf -o rw,uid=1000,gid=1000 shared $HOME/shared" >> /etc/rc.local'
#sudo sh -c 'echo "mount -t vboxsf -o rw,uid=1000,gid=1000 debian $HOME/debian" >> /etc/rc.local'
#sudo sh -c 'echo "exit 0" >> /etc/rc.local'

sudo addgroup $USER systemd-journal
