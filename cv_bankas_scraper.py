from bs4 import BeautifulSoup
import requests
import csv

CSV_FILE = "CV_BANKAS.csv"
URL = ['https://www.cvbankas.lt/?keyw=Python',
       'https://www.cvbankas.lt/?keyw=Python&page=2']


def get_access_and_data():
    data = []
    for url in range(0, 2):
        req = requests.get(URL[url]).text
        data.append(req)
    return str(data)


def parse_required_fields(data):
    result = []
    soup = BeautifulSoup(data, 'lxml')
    jobs = soup.find_all('article', class_='list_article list_article_rememberable jobadlist_list_article_rememberable')
    for index, job in enumerate(jobs, 1):
        job_item = {}
        job_item['index'] = index
        job_item['title'] = job.find('h3', class_='list_h3').text.replace('\\n', '').replace(' ', '')
        job_item['company_name'] = job.find('span', class_='dib mt5').text.replace('\\n', '').replace(' ', '')
        job_item['city_or_country'] = job.find('span', class_='list_city').text.replace('\\n', '').replace(' ', '')
        job_item['advertisement_link'] = job.find('a', class_='list_a can_visited list_a_has_logo') \
            .attrs['href'].replace('\\n', '')
        try:
            job_item['salary'] = job.find('span', class_='salary_amount').text.replace('\\n', '').replace(' ', '')
        except AttributeError:
            job_item['salary'] = ['not_specified']
        result.append(job_item)

    return result


def write_to_csv_file() -> None:
    jobs = get_access_and_data()
    with open(CSV_FILE, 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'Title', 'Company_Name',
                         'Country_or_City', 'Advertisement_link', 'Salary'])
        for job in parse_required_fields(jobs):
            writer.writerow(
                [job['index'],
                 job['title'],
                 job['company_name'],
                 job['city_or_country'],
                 job['advertisement_link'],
                 job['salary']])


write_to_csv_file()
