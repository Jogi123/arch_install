#!/usr/bin/env bash

# add new user
useradd -m jogi
usermod -aG wheel jogi
echo "Please enter password for jogi:"
passwd jogi
sed -i "s/# %wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/g" /etc/sudoers
pacman -S xdg-user-dirs --noconfirm --needed
xdg-user-dirs-update
rm /home/jogi/Public
rm /home/jogi/Templates
rm /home/jogi/Documents
rm /home/jogi/Music
rm /home/jogi/Videos

# install graphical utils
pacman -S xorg-server xorg-xrandr xf86-video-intel nvidia nvidia-utils nvidia-settings nvidia-lts nvidia-prime nvidia-smi sddm sddm-kcm --noconfirm --needed
systemctl enable sddm

# set german keyboard layout for sddm login screen
localectl set-x11-keymap de

# install audio
pacman -S pulseaudio pulseaudio-alsa alsa-utils --noconfirm --needed

# install bluetooth
pacman -S bluez bluez-utils pulseaudio-bluetooth --noconfirm --needed
systemctl enable bluetooth

# install kde
pacman -S plasma-desktop konsole dolphin firefox --noconfirm --needed

# install latte-dock
pacman -S latte-dock --noconfirm --needed

# install useful kde applets
pacman -S plasma-nm bluedevil plasma-pa powerdevil plasma-thunderbolt kscreen --noconfirm --needed

# install printing sofware
pacman -S hplip cups print-manager --noconfirm --needed
systemctl enable cups
cp /etc/cups/cupsd.conf /etc/cups/cupsd.conf.bak

# create gpg key for KDEWallet
gpg --full-gen-key

reboot
