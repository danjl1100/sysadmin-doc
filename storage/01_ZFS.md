# ZFS

## Prerequisites

* [Debian 10 installed](../os/01_Debian_Headless.md)


## Install ZFS-on-Linux
For Debian 10 (Buster), ZFS packages are [included in the contrib repo](https://wiki.debian.org/ZFS#Status).

1. Add Debian contrib repository to the apt sources.
    ```bash
    cp /etc/apt/sources.list sources.list.orig
    sudo sed -i 's/buster main$/buster main contrib/g' /etc/apt/sources.list
    ```
1. Update, install kernel headers and dependencies.
    ```bash
    sudo apt-get update
    sudo apt-get install dpkg-dev linux-headers-$(uname -r) linux-image-amd64
    ```
1. Install the zfs packages. May take a few minutes.
    ```bash
    sudo apt-get install zfs-dkms
    sudo modprobe zfs
    sudo apt-get install zfsutils-linux
    ```
1. Set ZFS module to load on boot.
    ```bash
    echo zfs | sudo tee /etc/modules-load.d/zfs.conf
    ```

Source: [zfsonlinux instructions](https://github.com/zfsonlinux/zfs/wiki/Debian)


## Create ZFS Pool

#### Tune `ashift` Parameter
Benchmark the drives with different `ashift` values, to find the optimal performance.
Source: [louwrentis.com](https://louwrentius.com/zfs-performance-and-capacity-impact-of-ashift9-on-4k-sector-drives.html)

1. Benchmark using `ashift=12`
    ```bash
    zpool create test -o ashift=12 mirror /dev/disk/by-id/... /dev/disk/by-id/...
    dd if=/dev/zero of=/test/ashift12.bin bs=1M count=100000
    # (e.g. I got 197 MB/s)
    zpool destroy test
    ```

1. Benchmark using `ashift=9`
    ```bash
    zpool create test -o ashift=9 mirror /dev/disk/by-id/... /dev/disk/by-id/...
    dd if=/dev/zero of=/test/ashift12.bin bs=1M count=100000
    # (e.g. I got 192 MB/s, slightly slower than above)
    zpool destroy test
    ```

1. Record the optimal `ashift` value for each `vdev`.

__NOTE__: Additional vdevs added to the pool can have their own `ashift` value.

#### Create Pool
1. ZFS pools cannot be resized without destroying and recreating the pool. To mitigate few-byte differences in disk sizes, we partition the disk with a tiny amount of trailing space.
    ```bash
    sudo parted /dev/disk/by-id/TARGET_DEVICE
    (parted) print
    # Verify this is the CORRECT DRIVE!!!
    (parted) mklabel gpt
    (parted) unit GB
    # this example: 4001 GiB drive, will leave 2 GiB free.
    (parted) mkpart primary 0 3999
    (parted) print free
    # Figure how much free space is left/available
    (parted) mkpart primary ext4 3999 4001
    (parted) print free
    # Double-check everything looks good
    (parted) quit
    ```

1. Repeat for all data drives.

1. Create the pool using the `ashift` value found in previous subsection.  
__NOTE:__ For simplicity, use pool name "`${HOSTNAME}`".
    ```bash
    sudo zpool create ${HOSTNAME} -o ashift=12 \
    mirror /dev/disk/by-id/.._1 /dev/disk/by-id/.._1
    ```

1. Verify ASHIFT and drive paths look correct.  Prefer canonical path `/dev/disk/by-id` rather than the volatile `/dev/sdX` notation.
    ```bash
    sudo zdb
    ```

1. Set properties for base dataset. Default to `lz4` compression and not tracking access times (`atime`).
    ```bash
    sudo zfs set compression=lz4 ${HOSTNAME}
    sudo zfs set atime=off ${HOSTNAME}
    ```


## Create ZFS Datasets

1. Create shared datasets.
    ```bash
    echo "movie music picture tv" > public_categories.txt
    sudo zfs create ${HOSTNAME}/public
    for category in `cat public_categories.txt`; do
        sudo zfs create ${HOSTNAME}/public/${category}
    done
    ```
    * Optionally, disallow creating uncategorized files: ```sudo chmod 550 /${HOSTNAME}/public```

1. Create datasets for each user with sane parameters.
    ```bash
    for user in $USER `cat users.txt`; do
        sudo zfs create ${HOSTNAME}/${user}
        sudo zfs create ${HOSTNAME}/${user}/safe
        sudo zfs set reservation=100G ${HOSTNAME}/${user}
        sudo zfs set refquota=100G ${HOSTNAME}/${user}/safe
        sudo zfs set quota=500G ${HOSTNAME}/${user}/safe
    done
    ```
    * Reserve 100G minimum for each user.
    * Limit `safe` folder to 100G (500G including snapshots).

1. Link to dataset in user homes, and set permissions.
    ```bash
    for user in $USER `cat users.txt`; do
        # link to USER and PUBLIC
        sudo ln -sn /${HOSTNAME}/${user} /home/${user}/${user}
        sudo ln -sn /${HOSTNAME}/public /home/${user}/public
        sudo chown -R ${user}:${user} /${HOSTNAME}/${user}
        sudo chmod -R a-w /${HOSTNAME}/${user}
        # reveal special directory: .zfs/snapshot
        sudo chown ${user}:${user} /${HOSTNAME}/${user}/{,safe/}.zfs{,/snapshot}
    done
    # sticky bit to make all PUBLIC files owned by `publisher`
    sudo chown -R nobody:publisher /${HOSTNAME}/public
    sudo chmod -R g+ws /${HOSTNAME}/public
    for category in `cat public_categories.txt`; do
        # reveal special directory: .zfs/snapshot
        sudo chown nobody:publisher /${HOSTNAME}/public/${category}/.zfs{,/snapshot}
    done
    ```


## Enhancements

### Auto-Snapshots
1. Install [zfs-auto-snapshot](https://github.com/zfsonlinux/zfs-auto-snapshot)
    ```bash
    wget https://github.com/zfsonlinux/zfs-auto-snapshot/archive/upstream/1.2.4.tar.gz
    tar -xzf 1.2.4.tar.gz
    cd zfs-auto-snapshot-upstream-1.2.4
    make install
    ```

1. Configure the crontab entries as desired
    ```bash
    for f in /etc/cron.*/zfs-auto-snapshot; do
        echo -e "===========================\n$f\n==========================="
        cat $f
    done
    ```

### Email Health Report

1. Setup the [ZFS health script](https://gist.github.com/petervanderdoes/bd6660302404ed5b094d) to run daily.
    ```bash
    wget https://gist.githubusercontent.com/petervanderdoes/bd6660302404ed5b094d/raw \
    -O - | sudo tee /etc/cron.daily/zfs_health
    sudo chmod +x /etc/cron.daily/zfs_health
    ```
    * __NOTE:__ failure output relies on root email setup.
1. Wait for the script to report `pool needs scrub` to verify it is working.
1. Schedule daily scrub of all pools
    ```bash
    echo "#!/bin/sh
    /sbin/zpool scrub ${HOSTNAME}" | sudo tee /etc/cron.daily/zpool_scrub
    sudo chmod +x /etc/cron.daily/zpool_scrub
    ```


## Next Steps

* Setup [Samba access](../services/02_Samba.md)


[Homepage](../README.md)
