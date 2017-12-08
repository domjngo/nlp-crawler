# Training
# import libraries
import functions
import guardian


def get_guardian_comments_summary(n):
    url = guardian.guardian_urls()
    all_article_urls = functions.get_all_article_urls(url, 'data-link-name', 'article')
    all_article_urls = list(set(all_article_urls))
    comment_summaries = []
    for link in all_article_urls:
        article = functions.get_article(link, 'div', 'class', 'content__article-body')
        if article:
            print(link)
            comment = functions.summarize(article, n, True, 140)
            print(comment)
            comment_summaries.append(comment)
    return comment_summaries


print(get_guardian_comments_summary(1))
