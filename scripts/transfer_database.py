from utils.opn import get_all_articles

from archi import Archi, ArticleData
import utils.opn as opn
from utils.opn import to_data, to_profile

from database import Article

from copy import deepcopy
import csv

articles = get_all_articles()

arc = Archi()
arc.load()
data = arc.data

subs_data = deepcopy(data)

# column = ['id', 'title', 'author', 'journal', 'year', 'doi', 'local_path', 'add_time']
# new_article = []
# for article in articles:
#     new_article.append([article.id, article.title, article.author, article.journal, article.year, article.doi, article.local_path, article.add_time])

# with open('articles.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(column)
#     for row in new_article:
#         writer.writerow(row)

# write to database
with open('articles.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        article = ArticleData(
            title=row['title'],
            author=row['author'],
            journal=row['journal'],
            year=row['year'],
            doi=row['doi'],
            local_path=row['local_path'],
            add_time=row['add_time']
        )
        article = opn.create_article(article)
        opn.add_article(article)
        id = article.id
        if not id == row['id']:
            for i, folder in enumerate(data):
                ids = [index for index, value in enumerate(folder["data"]) if value == int(row['id'])]
                for ii in ids:
                    subs_data[i]["data"][ii] = id

print(subs_data)
print(data)

# arc = Archi()
# arc.data = subs_data
# arc.save()

# opn.global_session().commit()