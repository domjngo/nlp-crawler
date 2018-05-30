# import libraries
from nltk.chat.util import Chat, reflections
import tweepy
import keys
import guardian
import data
import emoji
import pairs


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

    
def send_tweet(tweet):
    cfg = keys.cfg_keys()
    api = get_api(cfg)
    success = False
    try:
        print(tweet)
        status = api.update_status(status=tweet)
        success = True
        print(" => Successfully tweeted:")
    except:
        print(" => Tweet failed")
        pass
    return success


def search_twitter(search):
    cfg = keys.cfg_keys()
    api = get_api(cfg)
    results = [status for status in tweepy.
                     Cursor(api.search, q=search).items(100)]
    return results


def reply_tweet(results):
    cfg = keys.cfg_keys()
    api = get_api(cfg)
    selected_tweet = results[0]
    tweet = ("@{} This is a demo search for 'hello world' with a bot, hello"
             " world! #{}".format(selected_tweet.user.screen_name))
    tweet_id = selected_tweet.id
    api.update_status(tweet, tweet_id)


def reply(search='@starlord_p'):
    cfg = keys.cfg_keys()
    api = get_api(cfg)
    for tweet in tweepy.Cursor(api.search, search).items(1):
        try:
            tweetId = tweet.id
            username = tweet.user.screen_name
            text = tweet.text
            text = text.replace('@starlord_p ', '')
            phrase = Chat(pairs.eliza(), reflections).respond(text)
            api.update_status("@" + username + " " + phrase, in_reply_to_status_id=tweetId)
            print(tweet)
            print("Tweet : " + text)
            print("Replied with : " + phrase)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

reply()
