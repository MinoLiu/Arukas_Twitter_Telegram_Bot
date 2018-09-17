import telegram
import logging
import tweepy
import sys
from env import env
from utils import StdOutListener, StdOutStream

LOG = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] %(name)s: %(message)s',
    level=logging.INFO)

def auth_twitter():
    auth = tweepy.OAuthHandler(env('TWITTER_CONSUMER_KEY'), env('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(env('TWITTER_ACCESS_TOKEN'), env('TWITTER_ACCESS_TOKEN_SECRET'))
    return auth

if __name__ == '__main__':
    auth = auth_twitter()
    API = tweepy.API(auth)
    LOG.info('twitter api init success')
    twitter_ids = []
    for x in env('TWITTER_IDS'):
        try:
            user_obj = API.get_user(x)
        except Exception:
            print('Invalid twitter id, name. e.g. @kano_2525 or kano_2525')
            continue
        twitter_ids.append(user_obj.id_str)
    LOG.info('twitter id: {}'.format(twitter_ids))
    stream = StdOutStream(auth, StdOutListener(twitter_ids), retry_420=60)
    stream.filter(twitter_ids)
