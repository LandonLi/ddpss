FROM ubuntu

WORKDIR /app

ENV PYTHONUNBUFFERED 1
COPY api.py .
COPY run.py .
COPY requirements.txt .
COPY start.sh .

RUN sed -i "s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    sed -i "s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt update && \
    apt install -y python3-pip python3-venv && \
    python3 -m venv ./venv && \
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD /bin/bash -c "/app/start.sh"