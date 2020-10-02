# Docker

Sources: [Docker Engine (docs.docker.com)](https://docs.docker.com/engine/install/debian/#install-using-the-repository), [Docker Compose (docs.docker.com)](https://docs.docker.com/compose/install/)

## Prerequisites

* [Debian 10 installed](../os/01_Debian_Headless.md)


## Install Docker

1. Remove previous versions.
    ```bash
    sudo apt-get remove docker docker-engine docker.io containerd runc
    ```
1. Add docker repositories.
    ```bash
    sudo apt-get upgrade
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common
    
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
    
    # verify fingerprint is 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88
    sudo apt-key fingerprint 0EBFCD88
    
    echo "deb [arch=amd64] https://download.docker.com/linux/debian \
       $(lsb_release -cs) \
       stable" | sudo tee -a /etc/apt/sources.list.d/docker.list
    ```
1. Install docker engine.
    ```bash
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```
1. Verify the installation is working.
    ```bash
    sudo docker run --rm hello-world
    ```
1. Install docker-compose.
    ```bash
    # install current latest release (NOTE: CHECK FOR MORE RECENT VERSIONS FIRST)
    sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```


## Next Steps
```
#TODO
```


[Homepage](../README.md)
