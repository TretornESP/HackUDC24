FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    unzip \
    cmake \
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

WORKDIR /worker
USER buildbot

RUN wget https://codee.com/wp-content/uploads/2024/02/codee-2024.1.1-HackUDC.zip -O /worker/codee-2024.1.1-HackUDC.zip
RUN unzip /worker/codee-2024.1.1-HackUDC.zip -d /worker
RUN tar xzvf /worker/codee-2024.1.1-HackUDC/codee-2024.1.1-linux-x86_64.tar.gz -C /worker
RUN mv /worker/codee-2024.1.1-HackUDC/codee.lic /worker/codee-2024.1.1-linux-x86_64/
RUN rm /worker/*.zip
RUN rm /worker/*.tar.gz
RUN rm -rf /worker/codee-2024.1.1-HackUDC
RUN ln -s /worker/codee-2024.1.1-linux-x86_64/bin/pwdirectives /usr/local/bin/pwdirectives
RUN ln -s /worker/codee-2024.1.1-linux-x86_64/bin/pwloops /usr/local/bin/pwloops
RUN ln -s /worker/codee-2024.1.1-linux-x86_64/bin/pwreport /usr/local/bin/pwreport

COPY start.sh .
COPY runner.sh .
COPY extract_data.py .
COPY get_git.sh .

RUN find . 

RUN buildbot-worker create-worker . buildbot-master worker worker
CMD ["./start.sh"]