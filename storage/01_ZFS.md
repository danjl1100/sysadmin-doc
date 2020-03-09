# ZFS

## Prerequisites

* [Debian 10 installed](../os/01_Debian_Headless.md)


## Install ZFS-on-Linux
For Debian 10 (Buster), ZFS packages are included in the contrib repo.

1. Add Debian contrib repository to the apt sources.
```bash
cp /etc/apt/sources.list sources.list.orig
sudo sed -i 's/buster main$/buster main contrib/g' /etc/apt/sources.list
```
1. Update, install kernel headers and dependencies.
```bash
sudo apt update
sudo apt install dpkg-dev linux-headers-$(uname -r) linux-image-amd64
```

1. Install the zfs packages. May take a few minutes.
```bash
sudo apt install zfs-dkms
sudo modprobe zfs
sudo apt install zfsutils-linux
```

Source: [zfsonlinux instructions](https://github.com/zfsonlinux/zfs/wiki/Debian)


## Create Pool

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

#### Pool Creation
1. ZFS pools cannot be resized without destroying and recreating the pool. To mitigate few-byte differences in disk sizes, we partition the disk with a tiny amount of trailing space.
```bash
sudo parted /dev/disk/by-id/TARGET_DEVICE
(parted) print
# Verify this is the CORRECT DRIVE!!!
(parted) mklabel gpt
(parted) unit GB
(parted) mkpart primary 0 3999
(parted) print free
# Figure how much free space is left/available
(parted) mkpart primary ext4 3999 4001
(parted) print free
# Double-check everything looks good
(parted) quit
```

1. Create the pool using the `ashift` value found in previous subsection
```bash
sudo zpool create POOL_NAME -o ashift=12 \
mirror /dev/disk/by-id/.._1 /dev/disk/by-id/.._1
```
1. Verify ASHIFT and drive paths look correct.  Prefer canonical path `/dev/disk/by-id` rather than the volatile `/dev/sdX` notation.
```bash
sudo zdb
```

1. Set properties for base dataset. Default to `lz4` compression and not tracking access times (`atime`).
```bash
sudo zfs set compression=lz4 POOL_NAME
sudo zfs set atime=off POOL_NAME
```


## Create Datasets
```
#TODO
```


## Auto-Snapshots
```
#TODO
```


## Next Steps
```
#TODO
```


[Homepage](../README.md)
