FROM python:3.15-alpine

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
    && LDFLAGS="-L/usr/lib/graphviz -Wl,-rpath,/usr/lib/graphviz" \
    pip3 install --break-system-packages \
    gunicorn \
    pygraphviz \
    cryptography \
    dnspython \
    django \
    dnsviz \
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

