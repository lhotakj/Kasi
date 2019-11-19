FROM python:3.7-alpine

RUN mkdir -p /tmp/kasi/kasi

COPY kasi/ /tmp/kasi/kasi/
COPY LICENSE README.md requirements*.txt setup.py /tmp/kasi/

RUN python3 -m pip install /tmp/kasi
