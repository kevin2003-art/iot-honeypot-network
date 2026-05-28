FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git \
    libssl-dev \
    libffi-dev \
    build-essential \
    python3-dev \
    authbind \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash cowrie

USER cowrie

WORKDIR /home/cowrie

RUN git clone https://github.com/cowrie/cowrie.git cowrie

WORKDIR /home/cowrie/cowrie

RUN pip install --user -r requirements.txt

RUN cp etc/cowrie.cfg.dist etc/cowrie.cfg

EXPOSE 2222 2223

CMD ["bin/cowrie", "start", "-n"]
