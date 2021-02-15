FROM ubuntu

COPY api.py /app/
COPY run.py /app/
COPY requirements.txt /app/
COPY start.sh /app/

RUN apt update && \
    apt install -y python3-pip python3-venv && \
    python3 -m venv ./venv && \
    pip3 install -r /app/requirements.txt

CMD /bin/bash -c "/app/start.sh"