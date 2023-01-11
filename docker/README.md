### COMMANDS

- `docker build -t bios -f docker/Dockerfile .`
- `docker run -e GITHUB_TOKEN=<GITHUB_TOKEN> --rm -it --privileged --name bios bios:latest`

#### Note
- `privileged` needs to be there to access systemctl command inside docker