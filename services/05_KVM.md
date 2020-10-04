# Kernal Virtual Machine

Source: [wiki.debian.org](https://wiki.debian.org/KVM)

## Install KVM
1. Install qemu and libvirtd, ignoring related graphical packages.
    ```bash
    sudo apt-get install --no-install-recommends qemu-system libvirt-clients libvirt-daemon-system netcat-openbsd qemu-utils
    ```
    **Note:** netcat-openbsd is required due to quirk in virt-manager.
1. Allow regular user to manage virtual machines.
    ```bash
    sudo adduser $USER libvirt
    ```
1. Start the default (host-only) network.
    ```bash
    sudo apt-get install dnsmasq-base bridge-utils iptables
    virsh --connect=qemu:///system net-autostart default
    ```
1. Configure default URI for host startup/shutdown actions:
    ```bash
    sudo vi /etc/default/libvirt-guests
    # URIS=qemu:///system
    ```
1. On a debian desktop os, install virt-manager. Connect to the user previously granted, at uri qemu:///system
    ```bash
    sudo apt-get install virt-manager
    ```

## Next Steps

```
TODO
```


[Homepage](../README.md)
