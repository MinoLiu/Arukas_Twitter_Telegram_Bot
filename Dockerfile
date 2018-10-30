FROM python:3.6.6-alpine

LABEL maintainer="sean2525<madness48596@gmail.com>"

WORKDIR /app/src
COPY . /app/src

RUN set -e; \
    apk add --no-cache --virtual .build-deps \
    gcc \
    make \
    musl-dev \
    libc-dev \
    libffi-dev \
    openssl-dev \
    linux-headers \
    ; \
    pip3 install --no-cache-dir -U pip pipenv; \
    pipenv install --deploy --system; \
    pip3 uninstall pipenv -y; \
    apk del .build-deps;

# see source.env
ENV TWITTER_CONSUMER_KEY=
ENV TWITTER_CONSUMER_SECRET=
ENV TWITTER_ACCESS_TOKEN=
ENV TWITTER_ACCESS_TOKEN_SECRET=
ENV TWITTER_IDS=
ENV TELEGRAM_BOT_TOKEN=
ENV TELEGRAM_BOT_GROUPS=
ENV includeReplyToUser=False
ENV includeRetweet=False
ENV includeUserReply=False

CMD ["python3", "run.py"]