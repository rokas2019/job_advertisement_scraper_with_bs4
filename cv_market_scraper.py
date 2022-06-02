from bs4 import BeautifulSoup
import requests
import csv


CSV_FILE = 'job_data.csv'
CVMARKET_URL = 'https://www.cvmarket.lt'
URL = ['https://www.cvmarket.lt/joboffers.php?_track=index_click_job_search&op=search&search_location=landingpage'
       '&ga_track=homepage&search%5Bkeyword%5D=python&search%5Bexpires_days%5D=&search%5Bjob_lang%5D=&search%5Bsalary'
       '%5D=&search%5Bjob_salary%5D=3&mobile_search%5Bkeyword%5D=&tmp_city=&tmp_cat=&tmp_category=',

       'https://www.cvmarket.lt/joboffers.php?_track=index_click_job_search&op=search&search_location=landingpage'
       '&ga_track=homepage&search%5Bkeyword%5D=python&search%5Bexpires_days%5D=&search%5Bjob_lang%5D=&search%5Bsalary'
       '%5D=&search%5Bjob_salary%5D=3&mobile_search%5Bkeyword%5D=&tmp_city=&tmp_cat=&tmp_category=&start=30']

time_limit = 'prieš 1 mėn.'


def get_access_and_data():
    data = []
    for url in range(0, 2):
        req = requests.get(URL[url]).text
        data.append(req)
    return str(data)


def parse_required_fields(req):
    results = []
    soup = BeautifulSoup(req, 'lxml')
    jobs = soup.find_all('tr', class_='f_job_row2')
    for index, job in enumerate(jobs, 1):
        job_item = {}
        publish_date = job.find('div', class_='time-left-block').text
        if time_limit in publish_date:
            continue
        job_item['index'] = index
        job_item['title'] = job.find('a', class_='f_job_title main_job_link limited-lines') \
            .text.replace('\\n', '').replace(' ', '')
        job_item['company_name'] = job.find('span', class_='f_comp_title').text.replace('\\n', '')
        job_item['city_or_country'] = job.find('div', class_='f_job_city').text.replace('\\n', '').replace(' ', '')
        link = job.find('a', class_='f_job_title main_job_link limited-lines').attrs['href'].replace('\\n', '')
        job_item['advertisement_link'] = CVMARKET_URL + link

        try:
            salary = job.find('span', class_='f_job_salary').text.replace('\\n', '').replace(' ', '')
        except AttributeError:
            salary = 'not specified'

        job_item['salary'] = salary

        results.append(job_item)

    return results


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


