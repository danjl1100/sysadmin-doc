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
1. Create syncthing user.
    ```bash
    sudo adduser --disabled-password --gecos "" syncthing
    sudo usermod -a -G publisher syncthing
    ```
1. Grant syncthing permissions to write to bi-directional sync paths
    ```bash
    for user in $USER `cat users.txt`; do
        sudo chown -R ${user}:syncthing /${HOSTNAME}/${user}/safe
        sudo chmod g+ws /${HOSTNAME}/${user}/safe
    done
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
