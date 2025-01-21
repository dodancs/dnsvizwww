# python version higher than 3.11 does not have distutils
FROM python:3.11-alpine

RUN apk add \
    graphviz \
    ttf-liberation \
    bind \
    bind-tools \
    postgresql-libs \
    libpq \
    tzdata

RUN apk add --virtual builddeps \
    gcc \
    g++ \
    musl-dev \
    python3-dev \
    libffi-dev \
    make \
    postgresql-dev \
    graphviz-dev \
    openssl-dev \
    libc-dev \
    swig \
    py3-distutils-extra \
    \
    && pip3 install --break-system-packages \
    gunicorn==23.0.0 \
    pygraphviz==1.14 \
    cryptography \
    dnspython==2.2.1 \
    django==5.1.5 \
    dnsviz==0.11.0 \
    psycopg2 \
    \
    && apk del builddeps

COPY LICENSE /app/
COPY README.md /app/
COPY dnsvizwww /app/dnsvizwww
COPY manage.py /app/

COPY entrypoint.sh /

WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:8000", "dnsvizwww.wsgi"]

