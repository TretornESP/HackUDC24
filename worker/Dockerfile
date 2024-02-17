FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-venv \
    python3-wheel \
    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install 'buildbot[bundle]'

RUN groupadd -r buildbot && useradd -r -g buildbot buildbot
RUN mkdir /worker && chown buildbot:buildbot /worker
RUN mkdir /repository && chown buildbot:buildbot /repository
RUN mkdir /output && chown buildbot:buildbot /output
USER buildbot

WORKDIR /worker
COPY start.sh .
COPY runner.sh .
COPY extract_data.py .
COPY get_git.sh .

RUN buildbot-worker create-worker . buildbot-master worker worker
CMD ["./start.sh"]