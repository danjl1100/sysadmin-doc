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
```
#TODO
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
