# Kernal Virtual Machine

Source: [wiki.debian.org](https://wiki.debian.org/KVM)

## Install KVM
1. Install qemu and libvirtd, ignoring related graphical packages.
    ```bash
    sudo apt-get install --no-install-recommends qemu-system libvirt-clients libvirt-daemon-system virtinst netcat-openbsd qemu-utils
    ```
    **Note:** netcat-openbsd is required due to quirk in virt-manager run on controlling client machines.
1. Install packages for host-only networking.
    ```bash
    sudo apt-get install --no-install-recommends dnsmasq-base bridge-utils iptables ebtables
    sudo service libvirtd restart
    ```
    - If you use libvirt to manage your VMs, libvirt provides a NATed bridged network named "default" that allows the host to communicate with the guests. This network is available only for the system domains (that is VMs created by root or using the qemu:///system connection URI). VMs using this network end up in 192.168.122.1/24 and DHCP is provided to them via dnsmasq. This network is not automatically started. To start it use:
        ```bash
        virsh --connect=qemu:///system net-start default
        virsh --connect=qemu:///system net-autostart default
        ```
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
1. Test with a debian VM
    ```bash
    # from a DESKTOP PC with graphics
    LIBVIRT_DEFAULT_URI='qemu+ssh://USER@HOST/system' virt-install --virt-type kvm --name buster-amd64 --location http://deb.debian.org/debian/dists/buster/main/installer-amd64/ --os-variant debian10 --disk size=10 --memory 1000 --debug
    ```
1. On a desktop os, install virt-manager. Connect to the user previously granted, at uri qemu+ssh://USER@HOST/system
    ```bash
    sudo apt-get install virt-manager
    ```

## Enable PCI passthrough

Source: [wiki.archlinux.org](https://wiki.archlinux.org/index.php/PCI_passthrough_via_OVMF)

1. Install packages.
    ```bash
    sudo apt-get install pciutils
    ```
1. Verify IOMMU is enabled by bios.
    ```bash
    sudo dmesg | grep -i -e DMAR -e IOMMU
    ```
1. List IOMMU groups.
    ```bash
    #!/bin/bash
    shopt -s nullglob
    for g in /sys/kernel/iommu_groups/*; do
        echo "IOMMU Group ${g##*/}:"
        for d in $g/devices/*; do
            echo -e "\t$(lspci -nns ${d##*/})"
        done;
    done;
    ```



```
TODO:

nvidia geforce gtx 1050 Ti  10de:1c82
nvidia audio device 10de:0fb9

add to /etc/default/grub
	GRUB_CMDLINE_LINUX_DEFAULT="quiet vfio-pci.ids=10de:1c82,10de:0fb9"
then
	sudo update-grub

https://scottlinux.com/2016/08/28/gpu-passthrough-with-kvm-and-debian-linux/
Add vfio modules to initramfs image
sudo vim /etc/initramfs-tools/modules
add:
	vfio
	vfio_iommu_type1
	vfio_pci
	vfio_virqfd
rebuild initramfs
	sudo update-initramfs -u

reboot, verify vifo has taken hold of desired devices:
	sudo dmesg | grep -i vfio
	lspci -nnk -d [device:code]
	lspci -nnk -d [device:code]


https://wiki.archlinux.org/index.php/PCI_passthrough_via_OVMF
install ovmf
	sudo apt install ovmf
	sudo systemctl restart libvirtd


allow other computer's `virt-manager` to connect  
	# add user to libvirt group (required for QEMU+SSH connection, where sudo cannot be easily invoked)
	sudo usermod -a -G libvirt $(whoami)
	# verify libvirt group is listed
	id $(whoami) 
	# fix subtle bug, where remote clients expect `nc -U` to succeed (not allowed on netcat-universal package)
	sudo apt install netcat-openbsd



TODO:
* proper ZFS volume management:  https://libvirt.org/storage.html#StorageBackendZFS
* to cleanup visual glitches, add Nvidia driver in clover configurator:   https://www.tonymacx86.com/threads/gtx-1050ti-clover-configurator.220252/#post-1488683
* fix single-GPU rom issue with Nvidia cards (is this the issue I have??)   https://forums.unraid.net/topic/41951-gpu-passthrough-with-only-one-card/?do=findComment&comment=448403


```



## Next Steps

```
TODO
```


[Homepage](../README.md)
