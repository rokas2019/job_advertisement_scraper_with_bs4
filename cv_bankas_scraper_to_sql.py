import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3


pages = np.arange(1, 3, 1)


def get_data() -> list[str]:
    texts = []
    for page in pages:
        page = 'https://www.cvbankas.lt/?keyw=Python&page=' + str(page)
        text = requests.get(page).text
        texts.append(text)
    return texts


def parse_required_fields(texts) -> list[dict]:
    result = []
    texts = str(texts)
    soup = BeautifulSoup(texts, 'lxml')
    jobs = soup.find_all('article', class_='list_article list_article_rememberable jobadlist_list_article_rememberable')
    for index, job in enumerate(jobs, 1):
        job_item = {
            'index': index,
            'title': job.find('h3', class_='list_h3').text.replace('\\n', '').replace(' ', ''),
            'company_name': job.find('span', class_='dib mt5').text.replace('\\n', '').replace(' ', ''),
            'city_or_country': job.find('span', class_='list_city').text.replace('\\n', '').replace(' ', ''),
            'advertisement_link': job.find('a', class_='list_a can_visited list_a_has_logo') \
                .attrs['href'].replace('\\n', '')}
        try:
            job_item['salary'] = job.find('span', class_='salary_amount').text.replace('\\n', '').replace(' ', '')
        except AttributeError:
            job_item['salary'] = 0

        result.append(job_item)

    return result


def write_to_sql() -> None:
    conn = sqlite3.connect('test_database')
    c = conn.cursor()
    conn.commit()
    jobs = parse_required_fields(get_data())
    df = pd.DataFrame(jobs, columns=['index', 'title', 'company_name',
                                     'city_or_country', 'advertisement_link', 'salary'])
    df.to_sql('jobs', conn, if_exists='replace', index=False)
    c.execute('''
    SELECT * FROM jobs
    ''')

