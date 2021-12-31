ARG BASE_IMAGE_VERSION
FROM python:$BASE_IMAGE_VERSION-slim as build

RUN apt update -qq \
    && apt install git curl gcc g++ make file musl-dev libffi-dev zlib1g zlib1g-dev -y \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

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

FROM python:$BASE_IMAGE_VERSION-slim

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

RUN ./rubix-bios -p 1615 -g ./data/rubix-bios -d data -c config -a apps --install --prod --auth --device-type amd64

COPY docker/startup.sh ./

RUN chmod +x ./startup.sh

EXPOSE 1313 1414 1615 1616

CMD ["./startup.sh", "$GITHUB_TOKEN"]