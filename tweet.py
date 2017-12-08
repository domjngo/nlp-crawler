# import libraries
import tweepy
import keys
import guardian
import data
import emoji


# http://nodotcom.org/python-twitter-tutorial.html
def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def main():
    cfg = keys.cfg_keys()

    tweet_list = guardian.get_guardian_summary(1)

    sentiment = data.classifier.classify(data.extract_features(tweet_list[0][0].split()))

    if sentiment == 'negative':
        icon = emoji.emojize(':neutral_face:')
    elif sentiment == 'positive':
        icon = emoji.emojize(':thinking_face:')
    else:
        icon = ''

    api = get_api(cfg)
    tweet = tweet_list[0][0] + ' ' + icon + ' ' + ' #' + tweet_list[1] + ' #' + tweet_list[2] + ' #' + tweet_list[3]
    status = api.update_status(status=tweet)
