import codecs

import requests
from bs4 import BeautifulSoup as bs
from random import randint

__all__ = ('djini','work','dou')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def djini(url, city=None,language=None):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 3)])
        if resp.status_code == 200:
            soup = bs(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class':'list-jobs'})
            if main_ul:
                li_list = main_ul.find_all('li', attrs={'class':'list-jobs__item'})
                for li in li_list:
                    title = li.find('div', attrs={'class':'list-jobs__title'})
                    href = title.a['href']
                    if li.find('div', attrs={'class':'list-jobs__description'}).text:
                        content = li.find('div', attrs={'class':'list-jobs__description'}).text
                    company = li.find('div', attrs={'class':'list-jobs__details'}).text
                    # city = li.find('div', attrs={'class':'list-jobs__details'}).find('span',attrs={'class':'location-text'}).text

                    jobs.append({'title':title.text, 'url': domain + href,'description':content,'company': company,
                                'city_id':city, 'language_id':language})
                else:
                    errors.append({'url': url, 'title': 'Page do not response'})
        else:
            errors.append({'url':url, 'title':'Page do not response'})

    return jobs, errors


def work(url, city=None,language=None):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 3)])
        if resp.status_code == 200:
            soup = bs(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = div.find('div', attrs={'class': 'add-top-xs'}).span.b.text
                    # city = div.find('span', attrs={'class': 'middot'}).next_element.text
                    jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company,
                                'city_id':city, 'language_id':language
                                 })
                else:
                    errors.append({'url': url, 'title': 'Page do not response'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def dou(url, city=None,language=None):
    jobs = []
    errors = []
    domain = 'https://jobs.dou.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 3)])
        if resp.status_code == 200:
            soup = bs(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_list:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']
                    content = li.find('div', attrs={'class': 'sh-info'}).text

                    company = title.find('a', attrs={'class': 'company'}).text
                    # city = title.find('span', attrs={'class': 'cities'}).text
                    jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company,
                                'city_id':city, 'language_id':language
                                 })
                else:
                    errors.append({'url': url, 'title': 'Page do not response'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


if __name__ == "__main__":
    url = 'https://djinni.co/jobs/keyword-python/'
    jobs, errors = djini(url)
    h = codecs.open('work.json', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
