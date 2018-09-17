from envparse import Env

env = Env(
    TWITTER_CONSUMER_KEY=str,
    TWITTER_CONSUMER_SECRET=str,
    TWITTER_ACCESS_TOKEN=str,
    TWITTER_ACCESS_TOKEN_SECRET=str,
    TWITTER_IDS=dict(cast=list, subcast=str, default=[]),
    TELEGRAM_BOT_TOKEN=str,
    TELEGRAM_BOT_GROUPS=dict(cast=list, subcast=str, default=[]),
    includeReplyToUser=dict(cast=bool, default=False),
    includeRetweet=dict(cast=bool, default=False),
    includeUserReply=dict(cast=bool, default=False)
)