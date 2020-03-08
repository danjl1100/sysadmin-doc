# Debian Headless


## Installation Media

1. Download the [latest Debian netinstall release](https://www.debian.org/CD/netinst/), specifically `amd64`.
1. Flash image to USB drive
```
# dd if=debian-XX.X.X-amd64.netinst.iso of=TARGET_DEVICE bs=1M
```


## Installer Options

Boot into the non-graphical installer. Choose default (sane) options, noting these __specific details__:

#### System
1. Enter a sensible __lowercase hostname__. Prefer 2-3 syllables, and non-ambiguous spelling.
1. Blank domain name.
1. Leave __root password blank__, to disable the root account.  Prefer to use a normal-privileged user with sudoer rights instead.
1. Use the "single partition" guided method.  No real need for a separate `/home` parition when all storage will be handled by the storage driver.

#### Packages
1. Uncheck `Debian desktop environment` and `print server`.
1. Check only `SSH server` and `standard systems utilities`.


## Users Setup

1. Verify your login works.
1. For console-aesthetics reasons, force color prompt:
   ```
   $ sed -i 's/#force_color/force_color/g' ~/.bashrc
   $ source ~/.bashrc
   ```


## Fixing Issues

See headings below for how to address common issues.

#### Silencing `kvm: disabled by bios`
Create a `modprobe` conf file to blacklist the offending kvm modules:
```
$ echo "blacklist kvm
> blacklist kvm_intel
> blacklist kvm_amd" | sudo tee /etc/modprobe.d/blacklist-kvm.conf
```

Source: [askubuntu answer](https://askubuntu.com/a/312858)


## Next Steps

* Setup [SSH access](../services/01_SSH.md)


[Homepage](../README.md)
