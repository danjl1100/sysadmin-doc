# Debian Headless


## Installation Media

1. Download the [latest Debian netinstall release](https://www.debian.org/CD/netinst/), specifically `amd64`.
1. Flash image to USB drive.
    ```bash
    sudo dd if=debian-XX.X.X-amd64.netinst.iso of=/dev/TARGET_DEVICE bs=1M
    ```


## Installer Options

Boot into the non-graphical installer. Choose default (sane) options, noting these __specific details__:

#### System
1. Enter a sensible __lowercase hostname__. Prefer 2-3 syllables, and non-ambiguous spelling.
1. Leave __domain name blank__.
1. Leave __root password blank__, to disable the root account.  Prefer to use a normal-privileged user with sudoer rights instead.
1. Use the "single partition" guided method.  No need for a separate `/home` parition when all storage will be handled by the storage driver.

#### Packages
1. Uncheck `Debian desktop environment` and `print server`.
1. Check only `SSH server` and `standard systems utilities`.


## Initial Setup

1. Verify your login works.
1. For console-aesthetics reasons, force color prompt:
    ```bash
    sed -i 's/#force_color/force_color/g' ~/.bashrc
    source ~/.bashrc
    ```
1. Configure a static IP address (optional, but useful)
    ```bash
    sudo nano /etc/network/interfaces
    # CHANGE TO:
    #   auto INTERFACE_NAME
    #   iface INTERFACE_NAME inet static
    #   address 192.168.1.XXX
    #   gateway 192.168.1.1
    sudo service networking restart
    ```
1. Define the additional users you want to create.   This will be used in later steps.
    ```bash
    echo "user1 user2 user3" > users.txt
    ```
1. Create users with password login disabled (for now).
    ```bash
    for user in `cat users.txt`; do
    sudo adduser --disabled-password --gecos "" $user
    done
    ```
    * Configure passwords later with `sudo passwd USER`
1. Add users to publisher group.
    ```bash
    sudo groupadd publisher
    for user in $USER `cat users.txt`; do
        sudo usermod -a -G publisher $user
    done
    ```


## General Tools

1. Install these handy tools
    ```bash
    sudo apt install htop screen smartmontools parted
    ```


## Fixing Issues

See headings below for how to address common issues.

#### Silencing `kvm: disabled by bios`
Create a `modprobe` conf file to blacklist the offending kvm modules:
    ```bash
    echo "blacklist kvm
    blacklist kvm_intel
    blacklist kvm_amd" | sudo tee /etc/modprobe.d/blacklist-kvm.conf
    ```

Source: [askubuntu answer](https://askubuntu.com/a/312858)


## Next Steps

* Setup [SSH access](../services/01_SSH.md)


[Homepage](../README.md)
