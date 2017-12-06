# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
from heapq import nlargest
from collections import defaultdict


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
        article = clean_text(article)
        return article
    else:
        return ' '


def summarize(text, n):
    sentences = sent_tokenize(text)
    sentences = list(set(sentences))
    sentences = [x for x in sentences if len(x) < 110]

    my_stopwords = ['would', 'said', 'one', 'new', 'also', 'read', 'time', 'people', 'says', 'like', 'us', 'years']

    assert n <= len(sentences)
    words = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation) + my_stopwords)

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
    for div in text.find_all('div', {'class': 'block-share'}):
        div.decompose()
    text = text.text
    text = re.sub('\s+', ' ', text).strip()
    text = text.replace('–', '')
    text = text.replace('’', '')
    text = text.replace('“', '')
    text = text.replace('”', '')
    text = text.replace('|', '')
    return text
