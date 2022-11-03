FROM python:3.9-alpine3.13
LABEL maintainer='Omognuni'

ENV PYHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./account_book /account_book
WORKDIR /account_book
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --no-cache mariadb-connector-c-dev && \
    apk add --update --no-cache  --virtual .build-deps \
    gcc libffi-dev openssl-dev musl-dev mariadb-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .build-deps gcc libffi-dev musl-dev openssl-dev mariadb-dev && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER django-user