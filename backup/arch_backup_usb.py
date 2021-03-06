#!/bin/python

import os
import subprocess
import datetime

import configparser


class Arch_Backup:
    def __init__(self, base_command, include_list, exclude_list, source, destination, disk, mount_directory):
        self.base_command = base_command
        self.include_list = include_list
        self.exclude_list = exclude_list
        self.source = source
        self.destination = destination
        self.disk = disk
        self.mount_directory = mount_directory
        self.mount_backup_destination()
        self.start_time = datetime.datetime.now()
        self.backup()
        self.print_runtime()
        self.umount_backup_destination()

    def backup(self):
        """
        main function to backup specified directories, uses base_cmd string and appends the include/exclude options to
        the string
        """

        full_command = self.base_command
        for include in self.include_list:
            full_command += " " + "--include='" + str(include + "'")
        for exclude in self.exclude_list:
            full_command += " " + "--exclude='" + str(exclude) + "'"
        full_command += ' ' + str(self.source) + ' ' + str(self.destination)
        print(full_command)
        os.system(full_command)

    def mount_backup_destination(self):
        """
        first the luks encrypted drive will be opened and mounted afterwards at the specified mountpoint
        """

        subprocess.run(['sudo', '-S', 'cryptsetup', 'open', '/dev/sda4', 'backup'])
        subprocess.run(['sudo', '-S', 'mount', str(self.disk), str(self.mount_directory)])
        print('Drive successfully mounted')

    def umount_backup_destination(self):
        """
        first the drive will be unmounted from the specified mount directory and afterwards closed using cryptsetup
        """

        subprocess.run(['sudo', '-S', 'umount', str(self.mount_directory)])
        subprocess.run(['sudo', '-S', 'cryptsetup', 'close', 'backup'])
        print('Drive successfully unmounted')

    def print_runtime(self):
        """
        prints how long the backup took
        """

        end_time = datetime.datetime.now()
        runtime = end_time - self.start_time
        print('Backup took ' + str(runtime))


# load personal information from config file, named config_usb.ini
config = configparser.ConfigParser()
config.read('/home/jogi/programming/python/fun_projects/config_usb.ini')
base_cmd = 'rsync -av --delete --stats'
excl_lst = config['options']['exclude_list'].split(' ')
incl_lst = config['options']['include_list'].split(' ')
backup_source = config['paths']['backup_source']
backup_destination = config['paths']['backup_destination']
destination_disk = config['paths']['destination_disk']
mount_dir = config['paths']['mount_dir']


if __name__ == '__main__':
    backup = Arch_Backup(base_cmd, incl_lst, excl_lst, backup_source, backup_destination, destination_disk, mount_dir)
