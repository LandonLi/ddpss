FROM python:3.11-alpine

COPY api.py /app/
COPY run.py /app/
COPY requirements.txt /app/
COPY templates /app/templates
COPY static /app/static

RUN pip3 install --no-cache-dir -r /app/requirements.txt && \
    addgroup -S nonroot && \
    adduser -S nonroot -G nonroot

USER nonroot

CMD ["gunicorn", "--chdir", "/app/", "-b", "0.0.0.0:9145", "run:app"]
