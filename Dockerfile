FROM kennethreitz/pipenv:latest

WORKDIR /app/src
COPY . /app/src

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