ARG BASE_IMAGE_VERSION
FROM centos:latest as build

RUN yum update -y \
    && yum install python3 git curl gcc -y \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3

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

FROM centos:latest

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

COPY docker/startup.sh ./

RUN chmod +x ./startup.sh

RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -

RUN yum update -y \
    && yum install nodejs glibc-langpack-en -y

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 1414 1615 1616

CMD ["./startup.sh", "$GITHUB_TOKEN"]