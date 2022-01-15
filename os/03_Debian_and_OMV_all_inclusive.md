Motivation: OMV installer did not create a bootable drive at the end. Kept saying "Insert boot device and press any key" on multiple PCs.
Instead, these steps install Debian and then add OMV on top.


1. Install debian using net-install image
    1. Download debian net-install .iso file from https://www.debian.org/CD/netinst/
    1. Download [win32diskimager](https://sourceforge.net/projects/win32diskimager/) or similar (rufus?)
    1. Write the debian .iso to the USB drive.
    1. Boot the installer, then use the following install options:
        - NO grahical install
        - YES SSH server
        - Root password
        - Username: wayne (other users will be added later)
    1. Set static IP address to 192.168.1.51 (edit /etc/network/interfaces)
        1. TODO - add details
1. Install OMV using OMV-debian instructions
    https://openmediavault.readthedocs.io/en/5.x/installation/on_debian.html
1. Install OMV-Extras plugin, instructions on this site (easiest to install through Console/SSH)
    http://omv-extras.org/
1. Open the OMV control panel. This time, the default login was username: "admin" and password: "openmediavault".
    1. Change admin password to match Root password (for convenience). 
    1. Install ZFS plugin through OMV > Plugins menu
        1. search for package name "openmediavault-zfs"
        1. If the packages are broken, run these commands. hopefully this doesn't happen everytime...
            ```sh
            #print a list of not-configured packages
            dpkg -C

            # configure package zfs-dkms

            dpkg --configure zfs-dkms
            modprobe zfs

            # configure other dependent packages

            dpkg --configure zfsutils-linux
            dpkg --configure zfs-zed
            dpkg --configure openmediavault-zfs

            #verify the list is empty
            dpkg -C
            ```

    1. Add additional users to match the existing ZFS pool.
      - wayne (already created during debian OS installation)
      - julia (make this FIRST)
      - daniel (make this SECOND, to match existing ABRUMS ZFS pool)

1. Install zfs-auto-snapshot in the console. 
    1. Follow instructions here: https://github.com/zfsonlinux/zfs-auto-snapshot
        ```sh
        wget https://github.com/zfsonlinux/zfs-auto-snapshot/archive/upstream/1.2.4.tar.gz

        tar -xzf 1.2.4.tar.gz

        cd zfs-auto-snapshot-upstream-1.2.4

        make install
        ```
            
        Configuration is stored on the pool itself, so that should still be intact after installing this script.


    1. Verify the installation by checking: `zfs list -t snapshot` command output for recent timestamps.


1. Check the OMV settings against these screenshots:

    1. SMB CIFS Shares

        ![abrums_OVM_smb_cifs_shares](https://user-images.githubusercontent.com/45136864/149630951-db8430c5-4cc2-478b-992a-2506ea33f80f.png)

    1. SMB CIFS Settings

        ![abrums_OVM_smb_cifs_settings](https://user-images.githubusercontent.com/45136864/149630975-e3a77085-cad2-4efd-8459-834ebffc87c5.png)

    1. Shared Folders

        ![abrums_OVM_shared_folders](https://user-images.githubusercontent.com/45136864/149630984-8d35800b-dfeb-499b-9afd-b3f699250e52.png)

    1. Users

        ![abrums_OVM_users](https://user-images.githubusercontent.com/45136864/149631002-7f057493-028c-41e6-80e8-4b4e8aa4c162.png)

    1. ZFS Overview

        ![abrums_OVM_zfs_overview](https://user-images.githubusercontent.com/45136864/149631016-f80f9824-ec50-40f8-92e1-b9c7b889946e.png)

    1. OMV-Extras

        ![abrums_OVM_extras](https://user-images.githubusercontent.com/45136864/149631037-6b74bdc8-8f68-4f29-bad7-1fdfbf16709f.png)

    1. Plugins

        ![abrums_OVM_plugins_installed](https://user-images.githubusercontent.com/45136864/149631055-77e8129c-11a6-424f-8c64-d2630c0fd9b0.png)

    1. Notifications

        ![abrums_OVM_notifications](https://user-images.githubusercontent.com/45136864/149631102-8dfc5567-3b5d-478f-ac4b-8724927627fe.png)

    1. Network Inferfaces

        ![abrums_OVM_network_interfaces](https://user-images.githubusercontent.com/45136864/149631120-0c4547f0-30d6-4ea2-9dbf-3738128d3759.png)
