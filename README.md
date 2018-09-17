# Arukas_Twitter_Telegram_Bot
[![Docker hub](https://dockerbuildbadges.quelltext.eu/status.svg?organization=sean2525&repository=arukas_twitter_telegram_bot)](https://hub.docker.com/r/sean2525/arukas_twitter_telegram_bot/builds/)
[![license:mit](https://img.shields.io/badge/license-mit-blue.svg)](https://opensource.org/licenses/MIT)

A Telegram bot that forwards Tweets at Arukas
![0](https://i.imgur.com/qcgbW6Y.gif)

## Usage
### Config
``` env
# Twitter
export TWITTER_CONSUMER_KEY=
export TWITTER_CONSUMER_SECRET=
export TWITTER_ACCESS_TOKEN=
export TWITTER_ACCESS_TOKEN_SECRET=

# TWITTER_IDS can be screenname @XXXXXX XXXXXX
# ex:
# export TWITTER_IDS=github,docker
export TWITTER_IDS=

# Forwarding setting
export includeReplyToUser=False
export includeRetweet=False
export includeUserReply=False

# Telegram
export TELEGRAM_BOT_TOKEN=

# Bind chats can be multiple 
# ex:
# export TELEGRAM_BOT_GROUPS=-43223,340423,418230
# Q: How to find chat_id?
# Ans: https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
export TELEGRAM_BOT_GROUPS=
```

### Bash
``` bash
vim source.env # Fill it up
source source.env
pipenv install
pipenv run python run.py
```

### docker-compose
``` bash
vim docker-compose.yml # Fill it up
docker-compose up -d
```

### Arukas
* https://app.arukas.io 
Need to register account and credit card
![1](https://raw.githubusercontent.com/Sean2525/Arukas_Twitter_Telegram_Bot/master/img/1.png)
