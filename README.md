# Rubix BIOS

BIOS comes with default OS, non-upgradable

## Running in development

- Use [`poetry`](https://github.com/python-poetry/poetry) to manage dependencies
- Simple script to install

    ```bash
    ./setup.sh
    ```

- Join `venv`

    ```bash
    poetry shell
    ```

- Build local binary

    ```bash
    poetry run pyinstaller run.py -n rubix-bios-legacy --clean --onefile \
    --add-data VERSION:. \
    --add-data config:config \
    --add-data systemd:systemd
    ```

  The output is: `dist/rubix-bios-legacy`

## Deploy on Production

- Download release artifact
- Review help and start
```bash
./rubix-bios-legacy -h

Usage: run.py [OPTIONS]

Options:
  -p, --port INTEGER              Port  [default: 1615]
  -g, --global-dir PATH           Global data dir
  -d, --data-dir PATH             Application data dir
  -c, --config-dir PATH           Global config dir
  -a, --artifact-dir PATH         Artifact downloaded dir
  --prod                          Production mode
  --device-type [amd64|arm64|armv7]
                                  Device type  [default: armv7]
  --install                       Install rubix-bios-legacy
  --uninstall                     Uninstall rubix-bios-legacy
  --auth                          Enable JWT authentication
  -h, --help                      Show this message and exit.
```

### How To Install:

[See here for dockerized install](docker/README.md)

Download appropriate rubix-bios-legacy file from the [GitHub Release](https://github.com/NubeIO/rubix-bios-legacy/releases) & extract 
it, then run following command to start from systemd file:

- Template: 
    ```bash
    sudo ./rubix-bios-legacy -p <port> -g <global_dir> -d <data_dir> -c <config_dir> -a <artifact_dir> --device-type <device_type> --prod --install
    ```
- Template2 (With JWT authorization): 
  ```bash
  sudo ./rubix-bios-legacy -p <port> -g <global_dir> -d <data_dir> -c <config_dir> -a <artifact_dir> --device-type <device_type> --prod --install --auth
  ```
- To Run on BBB & Pi: 
    ```bash
    sudo ./rubix-bios-legacy -p 1615 -g /data/rubix-bios-legacy -d data -c config -a apps --prod --install
    ```
- To Run on BBB & Pi with auth restriction: 
    ```bash
    sudo ./rubix-bios-legacy -p 1615 -g /data/rubix-bios-legacy -d data -c config -a apps --prod --install --auth
    ```  
- To Run on Ubuntu: 
    ```bash
    sudo ./rubix-bios-legacy -p 1615 -g /data/rubix-bios-legacy -d data -c config -a apps --prod --install --device-type amd64
    ```    
- To Run on Ubuntu with auth restriction: 
    ```bash
    sudo ./rubix-bios-legacy -p 1615 -g /data/rubix-bios-legacy -d data -c config -a apps --prod --install --auth --device-type amd64
    ```   
- To Run on Ubuntu with auth restriction and GitHub token: 
    ```bash
    sudo ./rubix-bios-legacy -p 1615 -g /data/rubix-bios-legacy -d data -c config -a apps --prod --install --auth  --device-type amd64 --token <token>
    ```   

_**Note:** if bios installed with --auth, services will also open with same auth protection_

### How To Uninstall:

```bash
sudo ./rubix-bios-legacy --uninstall
```

### Authentication

> POST: `/api/users/login`
> Body
```json
{
    "username": "<username>",
    "password": "<password>"
}
```

> Use that `access_token` on header of each request

### Get Rubix Service releases
```bash
curl http://localhost:1615/api/service/releases
```

### Update check Rubix Service

```bash
curl http://localhost:1615/api/service/update_check
```

### Upgrade Rubix Service

```bash
curl -X PUT http://localhost:1615/api/service/upgrade -H "Content-Type: application/json" -d '{"version": latest|<version>}
```

### Upload artifact and Upgrade Rubix Service

```bash
curl -X PUT http://localhost:1615/api/service/upload_upgrade -H "Content-Type: multipart/form-data" -F "version=<version>" -F "file=<file>"
```

### Update Token if your Rubix Service repo is private

```bash
curl -X PUT http://localhost:1615/api/service/token -H "Content-Type: application/json" -d '{"token": <TOKEN>|null}'
```