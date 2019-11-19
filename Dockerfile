FROM python:3.7-alpine

ARG KASI_PORT=5000

RUN mkdir -p /tmp/kasi/kasi /opt/kasi

COPY kasi/ /tmp/kasi/kasi/
COPY LICENSE README.md requirements*.txt setup.py /tmp/kasi/
COPY docker/start.py /opt/kasi/

RUN python3 -m pip install /tmp/kasi && \
    rm -rf /tmp/kasi

EXPOSE $KASI_PORT

ENTRYPOINT [ "python3", "/opt/kasi/start.py" ]
