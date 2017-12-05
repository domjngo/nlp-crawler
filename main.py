# import libraries
import tweepy
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
from heapq import nlargest
from collections import defaultdict

print("Crawler 0.1")


def get_all_article_urls(url, att, value):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find(class_='facia-page')
    links = content.find_all('a', {att: value})
    url_list = []
    for link in links:
        url = link.get('href')
        url_list.append(url)
    return url_list


def get_article(url, element, att, value):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    article = soup.find(element, attrs={att: value})
    if article:
        return article.text
    else:
        return '. '


def summarize(text, n):
    sentences = sent_tokenize(text)
    sentences = list(set(sentences))
    sentences = [x for x in sentences if len(x) < 110]

    my_stopwords = ['would', 'said', 'one', 'new', 'also']

    assert n <= len(sentences)
    words = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english')+list(punctuation)+my_stopwords)

    new_words = [word for word in words if word not in _stopwords]
    freq = FreqDist(new_words)

    top_3 = nlargest(3, freq, key=freq.get)

    ranking = defaultdict(int)

    for i, sent in enumerate(sentences):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]

    sents_idx = nlargest(n, ranking, key=ranking.get)
    summary = [sentences[j] for j in sorted(sents_idx)]
    return [summary, top_3[0], top_3[1], top_3[2]]


def clean_text(text):
    text = text.replace('\n', ' ').strip()
    text = text.replace('–', '')
    text = text.replace('’', '')
    text = text.replace('“', '')
    text = text.replace('”', '')
    text = text.replace('|', '')
    return text


def get_guardian_summary(n):
    all_article_urls = get_all_article_urls('https://www.theguardian.com/uk', 'data-link-name', 'article')
    all_articles_text = ''
    for link in all_article_urls:
        article = get_article(link, 'div', 'class', 'content__article-body')
        print(link)
        all_articles_text += article
    all_articles_text = clean_text(all_articles_text)
    articles_summary = summarize(all_articles_text, n)
    return articles_summary


def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)


def main():
  # Fill in the values noted in previous step here
  cfg = {
    "consumer_key"        : "",
    "consumer_secret"     : "",
    "access_token"        : "",
    "access_token_secret" : ""
    }

  tweet_list = get_guardian_summary(1)

  api = get_api(cfg)
  tweet = tweet_list[0][0] + ' ' + ' #' + tweet_list[1] + ' #' + tweet_list[2] + ' #' + tweet_list[3]
  status = api.update_status(status=tweet)


if __name__ == "__main__":
  main()