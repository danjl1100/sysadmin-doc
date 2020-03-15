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
1. Add desired administrators users to `sudo` group.
    ```bash
    echo "user1 user2" > admins.txt
    for admin in `cat admins.txt`; do
        sudo adduser ${admin} sudo
    done
    ```


## General Tools

1. Install these handy tools
    ```bash
    sudo apt-get install htop screen smartmontools parted rsync
    ```

### Postfix Email
Route `root` emails to a gmail account. Source: [easyengine.io](https://easyengine.io/tutorials/linux/ubuntu-postfix-gmail-smtp)

1. Install packages
    ```bash
    sudo apt-get install postfix mailutils libsasl2-2 ca-certificates libsasl2-modules
    ```
    * Choose `Internet Site`, and keep the default entry for your hostname during the installation.
1. Edit postfix config `sudo nano /etc/postfix/main.cf` to add the following:
    ```
    relayhost = [smtp.gmail.com]:587
    smtp_sasl_auth_enable = yes
    smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
    smtp_sasl_security_options = noanonymous
    smtp_tls_CAfile = /etc/postfix/cacert.pem
    smtp_use_tls = yes
    ```
1. Create smtp credentials file.
    ```bash
    sudo nano /etc/postfix/sasl_passwd
    ```
    1. Use the following template:
        ```
        [smtp.gmail.com]:587    USERNAME@gmail.com:PASSWORD
        ```
    1. Restrict permissions, add to postmap.
        ```bash
        sudo chmod 400 /etc/postfix/sasl_passwd
        sudo postmap /etc/postfix/sasl_passwd
        ```
1. Fix errors with certificate validation.
    ```bash
    cat /etc/ssl/certs/thawte_Primary_Root_CA.pem | sudo tee -a /etc/postfix/cacert.pem
    sudo service postfix reload
    ```
1. Set alias for routing root mail to a specific user.
    ```bash
    echo "
    root: user1
    user1: you@example.com
    " | sudo tee -a /etc/aliases
    ```
    * Source: [brismuth.com](https://brismuth.com/scheduling-automated-zfs-scrubs-9b2b452e08a4)
1. Finally, test the configuration
    ```bash
    echo "Test mail from postfix, sent `date`" | mail -s "Test Postfix" you@example.com
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
