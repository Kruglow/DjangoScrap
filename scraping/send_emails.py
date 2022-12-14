import os, sys
import django
import datetime
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping.settings'

django.setup()
from scrap.models import Vacancy , Error, Url
from scraping.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER
today = datetime.date.today()
subject = f'Рассылка вакансий за {today}'
text_content = f'Рассылка вакансий {today}'
from_email = EMAIL_HOST_USER
empty = '<h2> На сегодня вакансий нет </h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'],i['language'])].append(i['email'])
if users_dct:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, date=today).values()[:5]
    vacancy = {}
    for i in qs:
        vacancy.setdefault((i['city_id'], i['language_id']), [])
        vacancy[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = vacancy.get(keys,[])
        html = ''
        for row in rows:
            html += f'<h5><a href="{ row["url"]}" target="_blank">{ row["title"] }</a></h5>'
            html += f'<p> {row["description"]} </p>'
            html += f'<p> {row["company"]} </p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

qs = Error.objects.filter(date=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors',[])

    for i in data:
        _html += f'<h5><a href="{ i["url"]}" target="_blank">Error: { i["title"] }</a></h5>'
    subject = f'Ошибки скрапинга {today}'
    text_content = f'Ошибки скрапинга {today}'



qs = Url.objects.all().values('city', 'language')
urls_dct = {(i['city'], i['language']):True for i in qs}
urls_errors = ''
for keys in users_dct.keys():
    if keys not in urls_dct:
        urls_errors += f'<h5>Для города :{keys[0]} и языка: {keys[1]} нет уплов!!!</h5>'
if urls_errors:
    subject += 'Отсутствуют урлы!!!'
    _html += urls_errors

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()

