import requests
from bs4 import BeautifulSoup
import re

url = 'https://cfetogo.tg/annonces-legales/details-annonce-2.html'
response = requests.get(url)

company = {}

soup = BeautifulSoup(response.content, 'html.parser')
main_page = soup.find('div', {'class': 'main'})

email_pattern = r'[a-zA-Z0-9]+[-._]*[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.[a-z]{2,}'
phone_number_pattern = r'([0-9]{8,13})|(\d{2} \d{2} \d{2} \d{2})'

emails = set(re.findall(email_pattern, main_page.get_text()))
if emails != set():
    company['email'] = [v for v in emails][0]
else:
    company['email'] = ''

phone_numbers = re.findall(phone_number_pattern, main_page.get_text())
formatted_numbers = set()
for phone_list in phone_numbers:
    for phone in phone_list:
        if phone:
            formatted_number = "+228" + phone.replace(" ", "")
            formatted_numbers.add(formatted_number)
if formatted_numbers != set():
    company['phone_number'] = [v for v in formatted_numbers][0]
else:
    company['phone_number'] = ''


p_list = main_page.find_all('p')
for p in p_list:
    for expr in [r'\Adenomination', r'\Aobjet', r'\Acapital social', r'\Asiege social', r'\Ageranc']:
        res = re.search(expr, p.get_text().lower())
        if res != None:
            company[expr[2:]] = res.string.split(':')[1]
            continue

company["name"] = str(company["denomination"]).lower().replace('«', '').replace('»', '').strip()

company["capital"] = re.search(r'\d+[.]*[ ]*\d{3}[.]*[ ]*\d{3}', main_page.getText()).group().replace(' ', '').replace('.', '')

if re.search('[lom]|[togo]', company['siege social']) != None:
    company["is_national"] = True
else:
    company["is_national"] = False

manager_pattern = re.compile(r'\b(mademoiselle|monsieur)\b [a-zA-Z]+( [a-zA-Z]+)*', re.IGNORECASE)
company['manager'] = re.search(manager_pattern, company['geranc']).group().upper()

for (k,v) in company.items():
    print(k, '->', v)