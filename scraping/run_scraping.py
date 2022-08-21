import asyncio
import codecs
import os, sys
import datetime as dt
from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping.settings'

import django
django.setup()

from django.db import DatabaseError
from scrap.parser import *
from scrap.models import Vacancy, City, Language, Error, Url

User = get_user_model()

parser = (
    (work, 'work'),
    (dou, 'dou'),
    (djini, 'djini')
)

jobs, errors = [], []
def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'],q['language_id']) for q in qs )
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'],q['language_id']):q['url_data'] for q in qs }
    urls = []
    for pair in _settings:
        if pair in url_dct:
            tmp = {}
            tmp['city']= pair[0]
            tmp['language']= pair[1]
            tmp['url_data']= url_dct[pair]
            urls.append(tmp)
    return urls

async def main(value):
    func, url,city,language = value
    job, err = await loop.run_in_executor(None,func,url,city,language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_lists = get_urls(settings)

# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()


# loop = asyncio.get_event_loop()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
tmp_task = [(func, data['url_data'][key], data['city'], data['language'])
            for data in url_lists
            for func, key in parser]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_task])

# for data in url_lists:
#     for func, key in parser:
#         url = data['url_data'][key]
#         j, e = func(url,city=data['city'],language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()
for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    qs = Error.objects.filter(date=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors:{errors}').save()

days_delate = dt.date.today() - dt.timedelta(10)
Vacancy.objects.filter(date__lte=days_delate).delete()