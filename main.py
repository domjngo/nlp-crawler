# import libraries
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.probability import FreqDist
from string import punctuation
from heapq import nlargest
from collections import defaultdict

print("Crawler 0.1")


def get_all_articles(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find(class_='facia-page')
    links = content.find_all('a')
    for link in links:
        print(link.prettify())


def get_article(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    article = soup.find('div', attrs={'class': 'content__article-body'}).text
    return article


def summarize(text, n):
    sentences = sent_tokenize(text)

    assert n <= len(sentences)
    words = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english')+list(punctuation))

    new_words = [word for word in words if word not in _stopwords]
    freq = FreqDist(new_words)

    # top_3 = nlargest(3, freq, key=freq.get)

    ranking = defaultdict(int)

    for i, sent in enumerate(sentences):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]

    sents_idx = nlargest(n, ranking, key=ranking.get)
    return [sentences[j] for j in sorted(sents_idx)]


# specify the url
url = 'https://www.theguardian.com/commentisfree/2017/dec/04/panorama-syria-allegations-uk-aid-transparency-bbc'

text = get_article(url).replace('\n', ' ').strip()
text = text.replace('–', '')
text = text.replace('’', '')
text = text.replace('“', '')
text = text.replace('”', '')
text = text.replace('|', '')

summary = summarize(text, 2)

print(summary)


page = urlopen('https://www.theguardian.com')
soup = BeautifulSoup(page, 'html.parser')
content = soup.find(class_='facia-page')
links = content.find_all('a')
for link in links:
    url = link.get('href')
    print(url)




# text = ' '.join(map(lambda p: p.text, soup.find_all('article')))

# article.encode('ascii', errors='replace').replace("?", " ")

# print(article.get_text())

# text = "Hello, my name is Nick. I like pineapple. I also like apples."

# words = [word_tokenize(sent) for sent in sents]

# bigram_measures = nltk.collocations.BigramAssocMeasures()
# finder = BigramCollocationFinder.from_words(wordsWOStopWords)
# print(sorted(finder.ngram_fd.items()))
