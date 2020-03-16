# Syncthing


## Install Package

Install stable Debian packages from [apt.syncthing.net](https://apt.syncthing.net/).

1. Add the release PGP keys:
    ```bash
    curl -s https://syncthing.net/release-key.txt | sudo apt-key add -
    ```

1. Add the "stable" channel to your APT sources:
    ```bash
    echo "deb https://apt.syncthing.net/ syncthing stable" | sudo tee /etc/apt/sources.list.d/syncthing.list
    ```

1. Update and install syncthing:
    ```bash
    sudo apt-get update
    sudo apt-get install syncthing
    ```

## Configure Autostart
1. Create syncthing user, adding to all groups it will sync files for.
    ```bash
    sudo adduser --disabled-password --gecos "" syncthing
    for usergroup in $USER `cat users.txt` publisher; do
        sudo usermod -a -G $usergroup syncthing
    done
    ```
1. Add group Read/Write/Sticky bit to ensure syncthing has permissions to write to sync paths.
    ```bash
    for user in $USER `cat users.txt`; do
        # GROUP: +Read +Write
        sudo chmod g+rw -R /${HOSTNAME}/${user}/safe
        # Directories GROUP: +Xecute +Sticky
        #  This copies group ownership to child items added to the folder.
        find /${HOSTNAME}/${user}/safe -type d -print0 | xargs -0 sudo chmod g+xs
    done
    ```
    * Note this distinction is important: Keep the files owned by the relevant user (non-syncthing) group, so that syncthing can create brand new files under that same group ownership.
    * Later, you can easily revoke `syncthing`'s permission by removing user `syncthing` from the relevant user-group.
        * e.g. Remove the `syncthing` user from the `publisher` group, disallowing write-access to public files, by the following:
            ```bash
            sudo deluser syncthing publisher
            ```
1. Enable System-service with syncthing user.
```bash
sudo systemctl enable syncthing@syncthing.service
sudo systemctl start syncthing@syncthing.service
```


## Next Steps

```
#TODO
```


[Homepage](../README.md)
