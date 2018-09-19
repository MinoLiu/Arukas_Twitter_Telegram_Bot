import logging
from time import gmtime, strftime

from tweepy.streaming import StreamListener
from tweepy.api import API
from tweepy import Stream
from telegram import Bot

from env import env

LOG = logging.getLogger(__name__)

bot = Bot(token=env('TELEGRAM_BOT_TOKEN'))


def telegram_publish(text, media_type, media_url):
    for x in env('TELEGRAM_BOT_GROUPS'):
        try:
            bot.send_message(
                x,
                text,
                'Markdown',
                True  # disable_web_page_preview
            )
            if media_type == 'video' or media_type == 'gif':
                bot.send_video(x, media_url)
            elif media_type == 'photo':
                bot.send_photo(x, media_url)
        except Exception as err:
            print(err)


def resolve_tweet(data):
    if 'retweeted_status' in data:
        data = data['retweeted_status']

    twitter_url = 'https://twitter.com/{}/status/{}'.format(data['user']['screen_name'], data['id_str'])

    text = ''

    if 'extended_tweet' in data:
        data = data['extended_tweet']
        text = data['full_text']
    else:
        text = data['text']

    for url in data['entities']['urls']:
        if url['expanded_url'] is None:
            continue
        text = text.replace(url['url'], "[%s](%s)" % (url['display_url'], url['expanded_url']))

    for userMention in data['entities']['user_mentions']:
        text = text.replace(
            '@%s' % userMention['screen_name'],
            '[@%s](https://twitter.com/%s)' % (userMention['screen_name'], userMention['screen_name'])
        )

    for hashtag in sorted(data['entities']["hashtags"], key=lambda k: k["text"], reverse=True):
        text = text.replace(
            '#%s' % hashtag['text'], '[#%s](https://twitter.com/hashtag/%s)' % (hashtag['text'], hashtag['text'])
        )

    media_replace = ''
    media_url = ''
    media_type = ''

    if 'media' in data['entities']:
        for media in data['entities']['media']:
            if media['type'] == 'photo' and not media_url:
                media_url = media['media_url_https']
                media_replace = media['url']
                media_type = 'photo'
            if media['type'] == 'video':
                media_replace = media['url']
                bitrate = 0
                for video in media['video_info']['variants']:
                    if 'bitrate' in video and video['bitrate'] >= bitrate:
                        bitrate = video['bitrate']
                        media_url = video['url']
                media_type = 'video'
            if media['type'] == 'animated_gif' and media_type != "video":
                media_replace = media['url']
                media_url = media['media_url_https']

    if 'extended_entities' in data and 'media' in data['extended_entities']:
        for media in data['extended_entities']['media']:
            if media['type'] == 'photo' and not media_url:
                media_url = media['media_url_https']
                media_replace = media['url']
                media_type = media['type']
            if media['type'] == 'video':
                media_type = media['type']
                bitrate = 0
                for video in media['video_info']['variants']:
                    if 'bitrate' in video and video['bitrate'] >= bitrate:
                        bitrate = video['bitrate']
                        media_url = video['url']
                media_replace = media['url']
            if media['type'] == 'animated_gif' and media_type != "video":
                media_type = 'gif'
                bitrate = 0
                for video in media['video_info']['variants']:
                    if 'bitrate' in video and video['bitrate'] >= bitrate:
                        bitrate = video['bitrate']
                        media_url = video['url']
                media_replace = media['url']

    if media_type != '':
        text = text.replace(media_replace, '\n{}'.format(twitter_url.replace('_', r'\_')))
    else:
        text = text + '\n{}'.format(twitter_url.replace('_', r'\_'))

    return text, media_type, media_url


class StdOutListener(StreamListener):
    def __init__(self, twitter_ids, api=None):
        self.api = api or API()
        self.twitter_ids = twitter_ids

    def on_status(self, status):
        """Called when a new status arrives"""

        data = status._json

        if data['user']['id_str'] not in self.twitter_ids:
            return True

        LOG.info(strftime("[%Y-%m-%d %H:%M:%S]", gmtime()) + " " + data['user']['screen_name'] + ' twittered.')
        worthPosting = False
        for twitter_id in self.twitter_ids:
            if data['user']['id_str'] != twitter_id:
                worthPosting = False
                if env('includeReplyToUser'):  # other Twitter user tweeting to your followed Twitter user
                    if data['in_reply_to_user_id_str'] == twitter_id:
                        worthPosting = True
            else:
                worthPosting = True
                # your followed Twitter users tweeting to random Twitter users
                # (relevant if you only want status updates/opt out of conversations)
                if env('includeUserReply') is False and data['in_reply_to_user_id'] is not None:
                    worthPosting = False

            if env('includeRetweet') is False:
                if 'retweeted_status' in data:
                    worthPosting = False  # retweet

            if not worthPosting:
                continue

        if not worthPosting:
            return True
        text, media_type, media_url = resolve_tweet(data)
        telegram_publish(text, media_type, media_url)

        return True

    def on_connect(self):
        """Called once connected to streaming server.

        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """
        LOG.info('Twitter stream success connected')
        return

    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        LOG.warning('Twitter stream on error({}) retry in few second.'.format(status_code))
        return

    def on_timeout(self):
        """Called when stream connection times out"""
        LOG.warning('Twitter stream connection times out')
        return

    def keep_alive(self):
        """Called when a keep-alive arrived"""
        LOG.debug('Twitter stream keep-alive')
        return


class StdOutStream(Stream):
    def __init__(self, auth, listener, **options):
        super().__init__(auth, listener, **options)

    def on_closed(self, resp):
        """ Called when the response has been closed by Twitter """
        LOG.warning('Twitter stream has been closed by Twitter')
        pass
