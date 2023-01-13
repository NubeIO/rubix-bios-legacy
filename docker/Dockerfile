ARG BASE_IMAGE_VERSION
FROM python:$BASE_IMAGE_VERSION-slim-buster as build

RUN apt update -qq
RUN apt install git -y
RUN apt install curl -y
RUN apt install gcc -y
RUN apt install g++ -y
RUN apt install make -y
RUN apt install file -y
RUN apt install musl-dev -y
RUN apt install libffi-dev -y
RUN apt install zlib1g -y
RUN apt install zlib1g-dev -y

COPY docker/get-poetry.py get-poetry.py
RUN POETRY_VERSION=1.1.13 python3 get-poetry.py

WORKDIR /usr/src/app/
ADD poetry.lock pyproject.toml ./
RUN $HOME/.poetry/bin/poetry install

ADD src src
ADD config config
ADD systemd systemd
ADD run.py VERSION ./
RUN $HOME/.poetry/bin/poetry run pyinstaller run.py -n rubix-bios --clean --onefile \
    --add-data VERSION:. \
    --add-data config:config \
    --add-data systemd:systemd

# slim is not supporting to install node, so we are using slim-buster
FROM python:$BASE_IMAGE_VERSION-slim-buster

ARG MAINTAINER="zero88 <sontt246@gmail.com>"
ARG APP_VERSION="1.0.0"
ARG RUBIX_UID=642
ARG NUBEIO_GID=1173
ARG COMMIT_SHA=$COMMIT_SHA

LABEL maintainer=$MAINTAINER version=$APP_VERSION commit=$COMMIT_SHA

ENV GLOBAL_DATA=/data

RUN mkdir -p /etc/systemd/system/multi-user.target.wants \
    && mkdir -p $GLOBAL_DATA

WORKDIR /usr/src/app/
COPY --from=build /usr/src/app/dist/rubix-bios ./
VOLUME $GLOBAL_DATA
ENV GITHUB_TOKEN="github_token"

RUN apt update -qq && apt install nodejs npm systemd systemd-sysv -y

RUN apt install cron -y

RUN ./rubix-bios -p 1615 -g ./data/rubix-bios -d data -c config -a apps --install --prod --auth --device-type amd64

COPY artifacts/rubix-edge-bios ./

RUN ./rubix-edge-bios install --arch=amd64 || echo "Ignore it for armv7"

COPY docker/startup.sh ./

RUN chmod +x ./startup.sh

CMD ["./startup.sh", "$GITHUB_TOKEN"]