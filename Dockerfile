FROM python:3.15-alpine

RUN apk add --no-cache \
    graphviz \
    ttf-liberation \
    bind \
    bind-tools \
    postgresql-libs \
    libpq \
    tzdata \
    && rm -rf /var/cache /root/.cache

RUN apk add --no-cache --virtual builddeps \
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
    pip3 install --break-system-packages --no-cache \
    gunicorn \
    pygraphviz \
    cryptography \
    dnspython \
    django \
    dnsviz \
    psycopg2 \
    \
    && apk del builddeps \
    && rm -rf /var/cache /root/.cache

COPY LICENSE /app/
COPY README.md /app/
COPY dnsvizwww /app/dnsvizwww
COPY manage.py /app/

COPY entrypoint.sh /

WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:8000", "dnsvizwww.wsgi"]

