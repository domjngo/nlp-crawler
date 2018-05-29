# import libraries
from nltk.chat.util import Chat, reflections
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


pairs = (
    (r'I\'m (.*)',
    ( "ur%1?? that's so cool! kekekekeke ^_^ tell me more!",
      "ur%1? neat!! kekeke >_<")),

    (r'(.*) don\'t you (.*)',
    ( "u think I can%2??! really?? kekeke \<_\<",
      "what do u mean%2??!",
      "i could if i wanted, don't you think!! kekeke")),

    (r'ye[as] [iI] (.*)',
    ( "u%1? cool!! how?",
      "how come u%1??",
      "u%1? so do i!!")),

    (r'do (you|u) (.*)\??',
    ( "do i%2? only on tuesdays! kekeke *_*",
      "i dunno! do u%2??")),

    (r'(.*)\?',
    ( "man u ask lots of questions!",
      "booooring! how old r u??",
      "boooooring!! ur not very fun")),

    (r'(cos|because) (.*)',
    ( "hee! i don't believe u! >_<",
      "nuh-uh! >_<",
      "ooooh i agree!")),

    (r'why can\'t [iI] (.*)',
    ( "i dunno! y u askin me for!",
      "try harder, silly! hee! ^_^",
      "i dunno! but when i can't%1 i jump up and down!")),

    (r'I can\'t (.*)',
    ( "u can't what??! >_<",
      "that's ok! i can't%1 either! kekekekeke ^_^",
      "try harder, silly! hee! ^&^")),

    (r'(.*) (like|love|watch) anime',
    ( "omg i love anime!! do u like sailor moon??! ^&^",
      "anime yay! anime rocks sooooo much!",
      "oooh anime! i love anime more than anything!",
      "anime is the bestest evar! evangelion is the best!",
      "hee anime is the best! do you have ur fav??")),

    (r'I (like|love|watch|play) (.*)',
    ( "yay! %2 rocks!",
      "yay! %2 is neat!",
      "cool! do u like other stuff?? ^_^")),

    (r'anime sucks|(.*) (hate|detest) anime',
    ( "ur a liar! i'm not gonna talk to u nemore if u h8 anime *;*",
      "no way! anime is the best ever!",
      "nuh-uh, anime is the best!")),

    (r'(are|r) (you|u) (.*)',
    ( "am i%1??! how come u ask that!",
      "maybe!  y shud i tell u?? kekeke >_>")),

    (r'what (.*)',
    ( "hee u think im gonna tell u? .v.",
      "booooooooring! ask me somethin else!")),

    (r'how (.*)',
    ( "not tellin!! kekekekekeke ^_^",)),

    (r'(hi|hello|hey) (.*)',
    ( "hi!!! how r u!!",)),

    (r'quit',
    ( "mom says i have to go eat dinner now :,( bye!!",
      "awww u have to go?? see u next time!!",
      "how to see u again soon! ^_^")),

    (r'(.*)',
    ( "ur funny! kekeke",
      "boooooring! talk about something else! tell me wat u like!",
      "do u like anime??",
      "do u watch anime? i like sailor moon! ^_^",
      "i wish i was a kitty!! kekekeke ^_^"))
    )


def reply(search):
    cfg = keys.cfg_keys()
    api = get_api(cfg)
    for tweet in tweepy.Cursor(api.search, search).items(1):
        try:
            tweetId = tweet.id
            username = tweet.user.screen_name
            print(tweet)
            text = tweet.text
            phrase = Chat(pairs, reflections).respond(text)
            api.update_status("@" + username + " " + phrase, in_reply_to_status_id=tweetId)
            print("Replied with " + phrase)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

reply('#kitten')
