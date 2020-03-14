# SSH


## Prerequisites
* [Debian installed](../os/01_Debian_Headless.md) with `openssh-server` (or equivalent) running


## Test Connection
1. Print the server's IP address and ECDSA fingerprint.
    ``` bash
    # on server
    ip addr show
    for f in /etc/ssh/*.pub; do ssh-keygen -lv -E sha256 -f $f; done
    ```
1. Connect from the client, verifying the ascii-art fingerprint matches.
    ``` bash
    # on client
    ssh -o visualhostkey=yes -o FingerprintHash=sha256 user@192.168.1.XXX
    ```
Source: adapted from [superuser answer](https://superuser.com/a/1442341)


## Public Key Authentication
Allowing only public key authentication makes the SSH server [more secure](https://security.stackexchange.com/a/3898).

#### Add Authorized Key(s)
1. If not already generated, make a key pair for your client.
    ```bash
    # on client
    ssh-keygen -t rsa
    # enter secure local passphrase
    ```
1. Copy the key to the remote server
    ```bash
    # on client
    ssh-copy-id user@192.168.1.XXX
    # enter password
    ```
1. Test the login
    ```bash
    # on client
    # requires only local passphrase, not password
    ssh user@192.168.1.XXX
    ```

Repeat this process for each user, from all clients.

#### Deny Password-Authentication

__NOTE:__ Wait until you have physical access to the server before trying this step. There's a risk of locking yourself out when configuring this remotely. You may need to manually re-enable password authentication from the physical server console.

1. Edit SSH config to deny password authentication.
    ```bash
    sudo nano /etc/ssh/sshd_config
    # change "PasswordAuthentication" from "yes" to "no"
    sudo service sshd reload
    ```


## Next Steps

* Setup [ZFS storage](../storage/01_ZFS.md)


[Homepage](../README.md)
