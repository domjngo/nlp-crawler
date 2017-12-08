# import libraries
import functions


def guardian_urls():
    urls = [
        'https://www.theguardian.com/uk',
        'https://www.theguardian.com/uk/environment',
        'https://www.theguardian.com/politics',
        'https://www.theguardian.com/music',
        'https://www.theguardian.com/lifeandstyle/health-and-wellbeing',
        'https://www.theguardian.com/artanddesign'
    ]
    return urls[4]


def get_guardian_summary(n):
    url = guardian_urls()
    all_article_urls = functions.get_all_article_urls(url, 'data-link-name', 'article')
    all_article_urls = list(set(all_article_urls))
    all_articles_text = ''
    for link in all_article_urls:
        article = functions.get_article(link, 'div', 'class', 'content__article-body')
        print(link)
        all_articles_text += article
    all_articles_text = all_articles_text
    articles_summary = functions.summarize(all_articles_text, n)
    return articles_summary
