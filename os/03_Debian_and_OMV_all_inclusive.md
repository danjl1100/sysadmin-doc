# Table of Contents
1. [Install](#Install)
1. [Settings](#Settings)
1. [ZFS Health Checks](#ZFS-Health-Checks)

Motivation: OMV installer did not create a bootable drive at the end. Kept saying "Insert boot device and press any key" on multiple PCs.
Instead, these steps install Debian and then add OMV on top.

## Install

1. Install debian using net-install image
    1. Before starting, identify (1) the INSTALLER usb drive, and (2) the TARGET boot drive (USB drive, hard drive, etc.).
        - Reasoning: The installer cannot install over itself, so there must be 2 drives.
        - PRO TIP: Pick a different sized drive for the TARGET, so it will be easy to find which drive to pick in the installer.
    3. Download debian net-install .iso file from https://www.debian.org/CD/netinst/
    4. Download [win32diskimager](https://sourceforge.net/projects/win32diskimager/) or similar (rufus?)
    5. Write the debian .iso to the INSTALLER usb drive.
    6. Boot the installer, then use the following install options:
        1. NO grahical install
        1. Hostname: `abrums`
        1. User Setup:
            - Root password
            - Username: wayne (other users will be added later)
        1. Partition/Disk Selection:
            - Guided - use entire disk
            - Select the TARGET drive, in the free space 
        1. Additional Software menu:
            - Uncheck Desktop and Gnome
            - Change SSH server to YES
            - If you accidentally install "desktop", you can remove it later by running `apt-get remove task-desktop xserver* && apt-get autoremove`
    7. Reboot when the installer asks you to.
    8. Manually set the IP address to static 192.168.1.51 (edit /etc/network/interfaces)
        1. Login as root
        1. Find the name of your network interface by running: `ip addr show`
        2. Run this command: `nano /etc/network/interfaces`
        3. Use the text editor to add the text block shown in these instructions below, changing the existing `dhcp` section if it exists.
            - `eth0` might be called something else like `enp20s0`, use the existing name instead of `eth0` in the snippet below.
            - Do not change any of the top lines referencing `lo` (localhost), just add after the `lo` section.
            ```conf
            auto eth0
            iface eth0 inet static
            address 192.168.1.51
            netmask 255.255.255.0
            gateway 192.168.1.1
            dns-nameservers 192.168.1.1
            ```
        4. After editing, use `Ctrl+O` and `Enter` to write the file (output the file). Then `Ctrl+X` to exit.
        5. Reboot by running this command: `reboot`
            - You can now use [PuTTY (on windows)](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) or [Connectbot (on Android)](https://play.google.com/store/apps/details?id=org.connectbot) to SSH to the server, connecting to `root@192.168.1.51` instead of manually typing at the computer's monitor/keyboard.
            - You can also keep using the computer's keyboard/monitor for the following steps. Your preference.
1. Install OMV using OMV-debian instructions
    https://openmediavault.readthedocs.io/en/5.x/installation/on_debian.html
1. Set/Verify the network settings in OMV control panel
    1. Open:  System > Network.  Interfaces tab. Look at the list of devices.
    2. If your network device IS LISTED, then Edit to verify the settings (especially DNS Servers) to match the step below.
    3. If your network device `enp1s0` (or your network device) is NOT listed, then click the "Add" button to add "Ethernet":
        - General settings
            - Pick your network device from the list
        - IPv4
            - Method = Static
            - Address = 192.168.1.51
            - Netmask = 255.255.255.0
            - Gateway = 192.168.1.1
        - IPv6 - disabled
        - Advanced Settings
            - DNS Servers = 8.8.8.8
            - (leave all other defaults)
3. Install OMV-Extras plugin, instructions on this site (easiest to install through Console/SSH)
    http://omv-extras.org/
1. Open the OMV control panel. This time, the default login was username: "admin" and password: "openmediavault".
    1. Change admin password to match Root password (for convenience). 
    1. Install ZFS plugin through OMV > Plugins menu
        1. search for package name "openmediavault-zfs"
        2. If installation succeeds, skip this step.
            Otherwise, if installation fails, or packages appear broken, then run these commands. Hopefully this doesn't happen everytime...
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

## Settings

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

## ZFS Health Checks

1. Use PuTTY to login to the server as user `root`
1. Run any of these commands to look at specific ZFS info:
    - (Lowest-level commands)
    - `zpool status` shows **drive status**, checksum errors (right-most column).
    - `zpool list` lists the pool **size usage**, fragmentation, and capacity. 
    - `zfs list` lists the ZFS-datasets (top-level **folders**) usage.
    - This command will list all the **snapshots**, sorted by the size used (biggest at the bottom)
        - `zfs list -rt snapshot | awk '{ print $2 " " $1}' | sort -h`
    - (Highest-level commands)

Examples:
1. `zpool status` - Healthy (error count all 0) and scrub shows no errors (scrub repaired 0B, within past week).
    - Ignore the "upgrade pool" status/action, this is irreversible not good for compatibility.
    - NOTE: Serial numbers obscured.
    ``` text
    [root@abrums:~]# zpool status
      pool: abrums
     state: ONLINE
    status: Some supported and requested features are not enabled on the pool.
        The pool can still be used, but some features are unavailable.
    action: Enable all features using 'zpool upgrade'. Once this is done,
        the pool may no longer be accessible by software that does not support
        the features. See zpool-features(7) for details.
      scan: scrub repaired 0B in 04:47:36 with 0 errors on Sun Nov 20 06:47:41 2022  <-- GOOD, scrubbed recently
    config:

        NAME                                         STATE     READ WRITE CKSUM
        abrums                                       ONLINE       0     0     0      <-- GOOD, zero drive errors
          raidz1-0                                   ONLINE       0     0     0
            ata-ST2000DM008-xxxxxx_xxxxxxxx          ONLINE       0     0     0
            ata-ST2000DM008-xxxxxx_xxxxxxxx          ONLINE       0     0     0
            ata-ST2000DM008-xxxxxx_xxxxxxxx          ONLINE       0     0     0
            ata-ST2000VX008-xxxxxx_xxxxxxxx          ONLINE       0     0     0
            ata-HGST_HUcccccccxxxxxx_xxxxxxxx-part1  ONLINE       0     0     0

    errors: No known data errors                                                     <-- GOOD, no data errors
    ```
1. `zpool list` - Fragmentation is OK, but nearing the maximum capacity. 
    - ZFS recommands staying under 80% capacity for max performance.
    ``` text
    [root@abrums:~]# zpool list
    NAME     SIZE  ALLOC   FREE  CKPOINT  EXPANDSZ   FRAG    CAP  DEDUP    HEALTH  ALTROOT
    abrums  9.06T  8.36T   723G        -         -    16%    92%  1.00x    ONLINE  -
    ```
1. `zfs list` - Shows the majority usage (5.95T out of 6.68T) is in `LARGE_ONE`.  The other datasets (top-level folders) only have a few hundred gigs of storage usage.
    - This includes usage from snapshots.
    - NOTE: Names obscured.
    ``` text
    [root@abrums:~]# zfs list
    NAME               USED  AVAIL     REFER  MOUNTPOINT
    abrums            6.68T   449G      166K  legacy
    abrums/LARGE_ONE  5.95T   449G     5.87T  legacy
    abrums/STUFF       350G   449G      350G  legacy
    abrums/SMALLER     195G   449G      195G  legacy
    abrums/SMALLEST    193G   449G      173G  legacy
                        ^^               ^^ Refer counts current (not-deleted) files
                        ^^ Used counts current + deleted files (in snapshots)
    ```
1. `zfs list -rt snapshot | awk '{ print $2 " " $1}' | sort -h`
    - NOTE: Names obscured.
    ``` text
    [root@abrums:~]# zfs list -rt snapshot | awk '{ print $2 " " $1}' | sort -h
    0B abrums/LARGE_ONE@zfs-auto-snap_daily-2021-12-04-1419
    0B abrums/LARGE_ONE@zfs-auto-snap_daily-2021-12-11-1349
    0B abrums/LARGE_ONE@zfs-auto-snap_daily-2021-12-12-1407
    0B abrums/LARGE_ONE@zfs-auto-snap_daily-2021-12-18-1415
    0B abrums/LARGE_ONE@zfs-auto-snap_daily-2021-12-25-1409
    0B abrums/LARGE_ONE@zfs-auto-snap_daily-2022-01-01-1341
    ...
    ... ~350 lines omitted ...
    ...
    10.6M abrums/SMALLEST@zfs-auto-snap_monthly-2021-05-15-1317
    14.2M abrums/SMALLEST@zfs-auto-snap_monthly-2021-01-19-1349
    74.7M abrums/LARGE_ONE@zfs-auto-snap_monthly-2021-09-13-1337
    310M abrums/LARGE_ONE@zfs-auto-snap_monthly-2021-01-19-1349
    594M abrums/SMALLEST@zfs-auto-snap_monthly-2021-10-13-1324
    18.2G abrums/LARGE_ONE@zfs-auto-snap_monthly-2021-10-13-1324
    ```
    - In this case, if you want to **destroy** a particular snapshot, you can run one command: `zfs` followed by `destroy` followed by the complete name of the snapshot (example: `abrums/LARGE_ONE@zfs-auto-snap_monthly-2021-01-19-1349`)
