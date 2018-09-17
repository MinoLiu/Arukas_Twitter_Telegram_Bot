FROM python:3.6-alpine

RUN apk update \
        && apk add --no-cache git openssh-client \
        && pip install pipenv \
        && addgroup -S -g 1001 app \
        && adduser -S -D -h /app -u 1001 -G app app

RUN mkdir /app/src
WORKDIR /app/src
RUN chown -R app.app /app/

USER app

COPY . /app/src

RUN set -ex && pipenv install --deploy --system

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

CMD ["python", "run.py"]