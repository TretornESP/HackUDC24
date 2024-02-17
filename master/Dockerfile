FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    python3-dev \
    python3-venv \
    python3-wheel \
    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install 'buildbot[bundle]'
RUN python3 -m pip install 'psycopg2'

RUN groupadd -r buildbot && useradd -r -g buildbot buildbot
RUN mkdir /master && chown buildbot:buildbot /master
RUN mkdir /repository && chown buildbot:buildbot /repository
USER buildbot

WORKDIR /master

COPY master.cfg .
COPY start.sh .
RUN buildbot checkconfig master.cfg

CMD ["./start.sh"]