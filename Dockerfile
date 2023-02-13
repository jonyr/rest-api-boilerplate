FROM python:3.10-slim-bullseye

ARG APP_DIR="/app"

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc curl \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean \
    && mkdir /var/log/gunicorn \
    && mkdir /home${APP_DIR} \
    && groupadd -g 999 python  \
    && useradd -d /home${APP_DIR} -r -u 999 -g python python \
    && chown python. /home${APP_DIR} \
    && chown python. /var/log/gunicorn

USER python

WORKDIR /home${APP_DIR}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --chown=python:python requirements.txt .

RUN pip install --no-warn-script-location --upgrade pip wheel setuptools \
    && pip install --no-warn-script-location --user --no-cache -r requirements.txt

ENV PATH="/home${APP_DIR}/.local/bin:$PATH"

COPY --chown=python:python . .

ENTRYPOINT ["./deployment/docker/entrypoint.sh"]

EXPOSE 8000
