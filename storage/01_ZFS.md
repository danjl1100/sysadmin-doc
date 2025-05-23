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
        # reveal special directory: .zfs/snapshot
        sudo chown ${user}:${user} /${HOSTNAME}/${user}/{,safe/}.zfs{,/snapshot}
    done
    # sticky bit to make all PUBLIC files owned by `publisher`
    sudo chown -R nobody:publisher /${HOSTNAME}/public
    sudo chmod -R g+ws /${HOSTNAME}/public
    # keep root level 'read-only'
    sudo chmod g-w /${HOSTNAME}/public
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
    sudo make install
    ```

1. Configure the anacron entries as desired
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
    # EDIT appropriately for Debian date params
    #  (line 111, choose Ubuntu option)
    sudo nano /etc/cron.daily/zfs_health
    sudo chmod +x /etc/cron.daily/zfs_health
    ```
    * __NOTE:__ failure output relies on root email setup.
1. Wait for the script to report `pool needs scrub` to verify it is working.
1. ~~Schedule daily scrub of all pools~~
    <pre><code><del> echo "#"'!'"/bin/sh
    /sbin/zpool scrub ${HOSTNAME}" | sudo tee /etc/cron.daily/zpool_scrub
    sudo chmod +x /etc/cron.daily/zpool_scrub</del></code></pre>
    * ~~__NOTE:__ monthly scrub is provided by `/etc/cron.d/zfsutils-linux`~~
    * Monthly scrub provided by zfsutils-linux has issues (can skip a month if system is powered down)
    * Better to use anacron:
    ```bash
    # comment-out the scrub line
    sudo vim /etc/cron.d/zfsutils-linux
    (echo '#!/bin/sh'; for pool in rpool bpool ${HOSTNAME}; do echo "/sbin/zpool scrub ${pool}"; done) | sudo tee /etc/cron.monthly/zpool_scrub
    sudo chmod +x /etc/cron.monthly/zpool_scrub
    ```

See [zfs_health_ignore_error](./zfs_health_ignore_error) for an example of ignoring a corruption error that you are OK with ignoring.

## Recipes

### Send and Receive Snapshots
Common commands to use for transferring datasets between two servers.

The example below uses server names `SENDER`/`RECEIVER`, pool names `SENDER_POOL`/`RECEIVER_POOL`, dataset `DATA`, and snapshot name `SNAPPED`.

1. If not yet done, snapshot the source folder.
    ```bash
    # on SENDER
    sudo zfs snapshot SENDER_POOL/DATA@SNAPPED
    ```
1. Prepare `RECEIVER` to accept the stream.
    ```bash
    # on RECEIVER
    mbuffer -s 128k -m 1G -I 9090 | sudo zfs recv -s -e RECEIVER_POOL
    ```
1. Initiate transfer from `SENDER`.
    ```bash
    # on SENDER
    sudo zfs send SENDER_POOL/DATA@SNAPPED | mbuffer -s 128k -m 1G -O RECEIVER:9090
    ```
1. If the transfer is interrupted, the `-s` flag saves the `RECEIVER`'s intermediate state and allows the transfer to resume later.

Source: [evercity.co.uk](https://everycity.co.uk/alasdair/2010/07/using-mbuffer-to-speed-up-slow-zfs-send-zfs-receive/)

### Auto Mirror

Use [zfs-auto-mirror](https://github.com/nadavgolden/zfs-auto-mirror) shell script to pull snapshots from the host.

1. Create users with limited rights: only zfs-send/-receive permissions for the datasets of interest.
    ```bash
    # on source host
    sudo useradd zfs-sender -m -s /bin/bash
    sudo passwd zfs-sender #create TEMPORARY password
    sudo zfs allow zfs-sender mount,snapshot,send,hold DATASET_PATHS
    ln -s /sbin/zfs /usr/bin/zfs

    # on destination host
    sudo useradd zfs-receiver -m -s /bin/bash
    sudo zfs allow zfs-receiver mount,create,receive DATASET_PATHS
    ln -s /sbin/zfs /usr/bin/zfs

    sudo -u zfs-receiver /bin/bash
    $ ssh-keygen -t rsa #create with no passphrase, in ~/.ssh/SOURCE_HOST.rsa
    $ echo "Host SOURCE_HOST
    	HostName SOURCE_HOST
    	IdentityFile ~/.ssh/SOURCE_HOST.rsa
    	User zfs-sender" >> ~/.ssh/config
    $ ssh-copy-id -i ~/.ssh/SOURCE_HOST.rsa.pub SOURCE_HOST
    $ exit

    # on source host
    sudo passwd -l zfs-sender
    ```
1. Download script on client.
    ```bash
    # on destination host
    sudo -u zfs-receiver /bin/bash

    wget https://raw.githubusercontent.com/nadavgolden/zfs-auto-mirror/master/zfs-auto-mirror.sh
    chmod +x zfs-auto-mirror.sh

    # apply fix for local snapshot detection (likely only needed for older zfsonlinux versions ~0.7.12)
    echo '141c141
    <     LOCAL_SNAPSHOTS=$(zfs list -t snapshot -H -S creation -o name ${LOCAL_DATASET} | grep ${LABEL} | cut -d "@" -f2-)
    ---
    >     LOCAL_SNAPSHOTS=$(zfs list -r -t snapshot -H -S creation -o name ${LOCAL_DATASET} | grep ${LABEL} | cut -d "@" -f2-)' | patch zfs-auto-mirror.sh
    ```
1. Setup mirroring as you wish, running commands like:
    ```bash
    sudo -u zfs-receiver /bin/bash
    $ ./zfs-auto-mirror.sh -p -d 1 SOURCE_HOST SOURCE_DATASET DESTINATION_DATASET
    ```

Source: [superuser.com](https://superuser.com/a/1483245)

### Expand a mirror by cloning to new drives (defrag)

Apparently ZFS does not have a built-in method to defragment the free space on the drives.  This should only matter for HDDs, where new files are forced to span a larger "seek distance" on the drive.

These steps assume expanding a from 8TB to 20TB, where the original 8TB drives will no longer be used. Adjust accordingly.

1. Ensure the source pool is not being written to (e.g. not mounted, no services querying ZFS)
    ```bash
    zfs set mountpoint=none mypool
    ```
1. Create the new pool:
    - destroy the existing partition tables:
        ```bash
        export NEW1=/dev/disk/by-id/drive-identifier1
        export NEW2=/dev/disk/by-id/drive-identifier2
        sudo fdisk -l $NEW1
        sudo fdisk -l $NEW2
        sudo fdisk $NEW1
        > g # create new GPT partition table
        > w # write changes to disk
        sudo fdisk $NEW2
        > g
        > w
        ```
	- create the new pool
        ```bash
        sudo zpool create -m none mypool-20 mirror $NEW1 $NEW2
        ```
	- setup the new pool to match the old one
        ```bash
        diff <(sudo zfs get all mypool | cut -d ' ' -f 2-) <(sudo zfs get all mypool-20 | cut -d ' ' -f 2-) -y | less
        sudo zfs set compression=lz4 mypool-20
        sudo zfs set atime=off mypool-20
        ```
	- clone the old pool to the new pool, using an appropriate SNAPSHOT name (e.g. transfer_YYYYMMDDTHHMM for the current time)
		```bash
		export SNAPSHOT="mypool@transfer_YYYYMMDDTHHMM"
		sudo zfs snapshot -r "$SNAPSHOT"
		# dry-run the send
		sudo zfs send -R "$SNAPSHOT" --dryrun --verbose
		# dry-run the receive
		sudo zfs send -R "$SNAPSHOT" | mbuffer -s 128k -m 1G | sudo zfs recv -Fdus mypool-20 -nv
		# execute for real
		sudo zfs send -R "$SNAPSHOT" | mbuffer -s 128k -m 1G | sudo zfs recv -Fdus mypool-20
		```
		- ZFS Send flags
			- -R recursive (send all child datasets/properties as well)
		- mbuffer flags
			- -s use blocks of this size (bytes) for the buffer
			- -m  total size (bytes) of the buffer
		- ZFS Receive flags
			- -F force a rollback of the receiving filesystem to the most recent snapshot
			- -d discard the first element from the received dataset name
			- -u do not mount the received datasets
			- -s if the stream is interrupted, print a "resume" token that can be used to resume the send
		```bash
		sudo zfs send -R "$SNAPSHOT" | mbuffer -s 128k -m 1G | sudo zfs recv -Fdus mypool-20    

		in @ 10.2 MiB/s, out @ 10.2 MiB/s, 2101 GiB total, buffer 100% fullin @ 100.0 MiB/s, out @ 100.0 MiB/s, 2678 GiB toin @  0.0 kiB/s, out @  0.0 kiB/s, 6178 GiB total, buffer   0% fulll, buffer   0% full

		summary: 6178 GiByte in 11h 11min 29.2sec - average of  157 MiB/s
		```
	- Rename the old pool
		```bash
		# rename the old pool to mypool-8
		sudo zpool export mypool
		sudo zpool import -d /dev/disk/by-id/ mypool mypool-8
		```
	- Rename the new pool into place
		```bash
		# rename the new pool from mypool-20 to mypool-8
		sudo zpool export mypool-20
		sudo zpool import -d /dev/disk/by-id/ mypool-20 mypool
		```
    - Verify the pool sizes look correct
        ```bash
        zpool list
        ```
1. Shutdown to physically disconnect the old `mypool-8` drives
1. Re-enable all known access to the zpool



## Next Steps

* Setup [Samba access](../services/02_Samba.md)


[Homepage](../README.md)
