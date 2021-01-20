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
    poetry run pyinstaller run.py -n rubix-bios --clean --onefile --add-data systemd:systemd
    ```

  The output is: `dist/rubix-bios`

## Deploy on Production

- Download release artifact
- Review help and start
```bash
./rubix-bios -h

Usage: run.py [OPTIONS]

Options:
  -p, --port INTEGER              Port  [default: 1514]
  -d, --data-dir PATH             Application data dir
  -g, --global-dir PATH           Global data dir
  -a, --artifact-dir PATH         Artifact downloaded dir
  --prod                          Production mode
  --device-type [amd64|arm64|armv7]
                                  Device type  [default: armv7]
  --install                       Install rubix-bios
  --uninstall                     Uninstall rubix-bios
  -h, --help                      Show this message and exit.
```

### How To Install:

Download appropriate rubix-bios file from the [GitHub Release](https://github.com/NubeIO/rubix-bios/releases) & extract 
it, then run following command to start from systemd file:

- Template: 
    ```bash
    sudo ./rubix-bios -p <port> -d <data_dir> -g <global_dir> -a <artifact_dir> --device-type <device_type> --prod --install
    ```
- To Run on BBB & Pi: 
    ```bash
    sudo ./rubix-bios -p 1514 -d /data/rubix-bios -g /data -a /data/rubix-bios/apps --prod --install
    ```
    

### How To Uninstall:

```bash
sudo ./rubix-bios --uninstall
```
