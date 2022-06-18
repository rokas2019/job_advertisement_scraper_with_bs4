import numpy as np
from bs4 import BeautifulSoup
import requests
import csv

CSV_FILE = "CV_BANKAS.csv"
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
            job_item['salary'] = 'not specified'

        result.append(job_item)

    return result


def write_to_csv_file() -> None:
    jobs = parse_required_fields(get_data())
    with open(CSV_FILE, 'a', encoding="utf-8") as f:
        field_names = ['Index', 'Title', 'Company_Name',
                       'Country_or_City', 'Advertisement_link', 'Salary']
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        list_index = 1
        for job in jobs:
            writer.writerow(
                {'Index': job.get('index'),
                 'Title': job.get('title'),
                 'Company_Name': job.get('company_name'),
                 'Country_or_City': job.get('city_or_country'),
                 'Advertisement_link': job.get('advertisement_link'),
                 'Salary': job.get('salary')
                 })
            list_index += 1


write_to_csv_file()
