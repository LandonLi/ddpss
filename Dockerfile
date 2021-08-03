FROM python:3.8-alpine

COPY api.py /app/
COPY run.py /app/
COPY requirements.txt /app/
COPY templates /app/templates
COPY static /app/static

RUN apk add --update --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip3 install --no-cache-dir -r /app/requirements.txt && \
    apk del .build-deps

CMD ["gunicorn", "--chdir", "/app/", "-b", "0.0.0.0:9145", "run:app"]
