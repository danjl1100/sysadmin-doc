# Samba

## Prerequisites

* [Debian 10 installed](../os/01_Debian_Headless.md)
* [ZFS storage](../storage/01_ZFS.md) is required for ["Restore Previous Versions" feature](#zfs-integration)


## Install Samba

```bash
sudo apt-get install samba
```

## Configure Shares

1. Comment out all the existing share lines `sudo nano /etc/samba/smb.conf`
    ```
    ;[homes]
    ;[netlogon]
    ;[profiles]
    ;[printers]
    ;  etc...
    ```
1. Add public shares:
    ```bash
    echo "
    [public]
            comment = Public Files
            browseable = yes
            read only = no
            path = /${HOSTNAME}/public
            guest ok = no
            valid users = $USER `cat users.txt`
            create mask = 0775
            force create mode = 0775
            directory mask = 0775
            force directory mode = 0775
    " | sudo tee -a /etc/samba/smb.conf
    ```
1. Add user shares:
    ```bash
    for user in $USER `cat users.txt`; do
    echo "
    [${user}]
            comment = ${user}
            browseable = no
            read only = no
            path = /${HOSTNAME}/${user}
            guest ok = no
            valid users = ${user}
            create mask = 0775
            force create mode = 0775
            directory mask = 0775
            force directory mode = 0775
    " | sudo tee -a /etc/samba/smb.conf
    done
    ```
1. Add users to Samba
    ```bash
    for user in $USER `cat users.txt`; do
        sudo smbpasswd -a ${user}
    done
    ```
1. Restart Samba: `sudo service smbd restart`

## ZFS Integration
Add `zfs-auto-snapshot` hook for _Restore Previous Versions_ feature on windows clients.  
Source: [github.com/zfsonlinux](https://github.com/zfsonlinux/zfs-auto-snapshot/wiki/Samba) and [samba.org](https://www.samba.org/samba/docs/current/man-html/vfs_shadow_copy2.8.html)

1. Edit Samba config: `sudo nano /etc/samba/smb.conf`
1. Add the following in the `[global]` section. ___NOT___ below any share definition.
    ```
    ;# allow ZFS snapshots to show up in 'Restore Previous Versions'
    vfs objects = shadow_copy2
    shadow: snapdir = .zfs/snapshot
    shadow: sort = desc
    shadow:snapdirseverywhere = yes
    shadow: format = -%Y-%m-%d-%H%M
    shadow: snapprefix = ^zfs-auto-snap_\(frequent\)\{0,1\}\(hourly\)\{0,1\}\(daily\)\{0,1\}\(monthly\)\{0,1\}
    shadow: delimiter = -20
    ```
1. Restart Samba: `sudo service smbd restart`



## Next Steps

* Explore [extras](../README.md#extras)


[Homepage](../README.md)
