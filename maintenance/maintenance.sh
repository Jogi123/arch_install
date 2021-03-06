#!/bin/bash

# update mirrorlist
sudo cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak
sudo pacman -S reflector --noconfirm --needed
sudo reflector --verbose --latest 10 --sort rate --save /etc/pacman.d/mirrorlist

# update system
sudo pacman -Syu --noconfirm

# clean cached pacman (delete all uninstalled cached packages and only 2 older versions of installed packages)
sudo pacman -S pacman-contrib --noconfirm --needed
sudo paccache -ruk0
sudo paccache -rk3
sudo pacman -Rns $(pacman -Qtdq) --noconfirm

# clean chached files and logs
sudo rm -rf ~/.cache/*
sudo journalctl --vacuum-time=2weeks
