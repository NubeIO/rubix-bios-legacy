### COMMANDS

- `docker build -t bios -f docker/Dockerfile .`
- `docker run -e GITHUB_TOKEN=<GITHUB_TOKEN> --rm -it -p 1615:1615 -p 1616:1616 -p 1414:1414 --privileged --name bios bios:latest`

#### Note
- `privileged` needs to be there to access systemctl command inside docker