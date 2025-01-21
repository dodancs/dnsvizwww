# DNSVIZ web view

This is a fork of the original [dnsvizwww](https://github.com/dnsviz/dnsvizwww) project, that aims to bring the project to life and provide a Docker image which anyone can deploy.

Originally, the project is provided as-is, and many files and configurations are missing, which means, you cannot run it directly. I have ventured into the deep depths of 'how to run a Django app' and I was successful! I guess if anyone else wants to deploy dnsviz in their own infra, not relying on the public https://dnsviz.net service, you can do so now.

## Installing

Everything is in Docker, the project has the `Dockerfile` used to build the image, and an example `docker-compose.yml` with `env.example`. You may opt to build the image yourself from the source code, so here is how you do that:

```bash
$ git clone https://github.com/dodancs/dnsvizwww.git
$ cd dnsvizwww
$ docker-compose build
$ docker-compose up -d
```

By default the `docker-compose.yml` is set to build the image locally:

```yaml
  dnsviz:
    image: ghcr.io/dodancs/dnsvizwww:local
    restart: always
    build:
      context: .
```

But, if you want to use a pre-made image, I have them published here on Github in the [packages section](https://github.com/dodancs/dnsvizwww/pkgs/container/dnsvizwww), so you may use:

```yaml
  dnsviz:
    image: ghcr.io/dodancs/dnsvizwww:latest
    restart: always
    #build:
    #  context: .
```

It is better to put your local changes into `docker-compose.override.yml` as that won't interfere with this repository, see https://github.com/dodancs/dnsvizwww?tab=readme-ov-file#changes-to-docker-compose-yml.

After modifying the `docker-compose.yml` file, just bring the containers up, or pull the images before hand:

```bash
$ docker-compose pull
$ docker-compose up -d
```

## Configuration

The main configuration file is `dnsvizwww/settings.py`, and it is ready to be deployed as is, because anything that would be user-configurable is exposed as an environment variable that you can set in deployment.

### Setting up environment variables

Copy the `env.example` file to `.env` and check it out:

```bash
$ cp env.example .env
$ vim .env
```

```ini
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=dnsviz
POSTGRES_USER=dnsviz
POSTGRES_PASSWORD=secret

SECRET_KEY=secret

ALLOWED_HOSTS=dnsviz.example.com

DEBUG=true

TZ=Americas/Detroit
```

By default, the container uses PostgreSQL as its backend for data, so the `docker-compose.yml` also reflects this. You only need to change the `POSTGRES_PASSWORD` value to be extra safe.

Other than that, be sure to change the `SECRET_KEY` value to something strong, for example you can use the output of openssl like so:

```bash
$ openssl rand -base64 48
n+0gPnasv3fCeFd1tKil09kMYBYwefmApssL9/ooEWaDA506tbED+Zhz6gQWoqyc
```

And set the `SECRET_KEY`:

```ini
SECRET_KEY=n+0gPnasv3fCeFd1tKil09kMYBYwefmApssL9/ooEWaDA506tbED+Zhz6gQWoqyc
```

If you use a reverse proxy for the container, with NginX or Traefik, be sure to add your domain names into `ALLOWED_HOSTS` separated with a comma `,`, otherwise you will not be able to access dnsviz:

```ini
ALLOWED_HOSTS=dnsviz.example.com,dnsviz.int.example.com
```

Also as you prefer, you may change the timezone:

```ini
TZ=Americas/Detroit
```

### Changes to `docker-compose.yml`

By default the database container stores its files to `./data`, but you may change it and use volumes. To do this, do not edit the `docker-compose.yml` file directly, but rather create an override file:

```bash
$ vim docker-compose.override.yml
```

```yaml
services:
  db:
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

