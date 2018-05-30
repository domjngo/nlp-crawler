import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from nltk.chat.util import Chat, reflections
import keys
import pairs

cfg = keys.cfg_keys()
auth = OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])


def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def reply(tweet):
    cfg = keys.cfg_keys()
    api = get_api(cfg)
    try:
        tweetId = tweet.id
        username = tweet.user.screen_name
        text = tweet.text
        text = text.replace('@starlord_p ', '')
        phrase = Chat(pairs.eliza(), reflections).respond(text)
        api.update_status("@" + username + " " + phrase, in_reply_to_status_id=tweetId)
        print("Tweet : " + text)
        print("Replied with : " + phrase)
    except tweepy.TweepError as e:
        print(e.reason)


class listener(StreamListener):

    def on_status(self, data):
        print(data)
        reply(data)
        return (True)

    def on_error(self, status):
        print(status)


twitterStream = Stream(auth, listener())
twitterStream.filter(track=["@starlord_p"])
