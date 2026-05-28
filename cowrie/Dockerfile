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

WORKDIR /home/cowrie

RUN git clone https://github.com/cowrie/cowrie.git cowrie

WORKDIR /home/cowrie/cowrie

RUN pip install -r requirements.txt

RUN pip install .

RUN cp etc/cowrie.cfg.dist etc/cowrie.cfg || true

RUN chown -R cowrie:cowrie /home/cowrie

USER cowrie

ENV PATH="/home/cowrie/.local/bin:${PATH}"
ENV PYTHONPATH="/home/cowrie/cowrie/src"

EXPOSE 2222 2223

CMD ["twistd", "-n", "cowrie"]
