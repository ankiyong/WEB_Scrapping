import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find('div', {'class': 'pagination'})
    links = pagination.find_all('li')
    spans = []
    for link in links[:-1]:
        spans.append(int(link.string))
    # pages는 list기 때문에 for문을 통해 문자열을 추출하는  것이다.
    max_page = spans[-1]
    return max_page


def extract_job(html):
    title = html.find('h2', {
        'class': 'jobTitle'
    }).find('span', title=True).string
    #title속성을 가지고 있는 span을 출력해라
    company = html.find('span', {'class': 'companyName'}).string
    location = html.find('div', {'class': 'companyLocation'}).get_text()
    job_id = html.parent.parent.parent.parent.parent['href']
    #아래 설정되어있는 html주소보다 5단계 위에 위치한 부모 태그를 찾기 위해 parent를 5번 사용헀다
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f'https://www.indeed.com{job_id}'
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping INDEED : page {page}')
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('table', {'class': 'jobCard_mainContent'})
        for titles in results:
            job = extract_job(titles)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
