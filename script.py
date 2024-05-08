import requests
from bs4 import BeautifulSoup
import re
import csv

url = 'https://cfetogo.tg/annonces-legales/details-annonce-2.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
main_page = soup.find('div', {'class': 'main'})

company = {}

sector = {'is_import_export': r'import[ ]*-[ ]*export', 'is_transport': 'transport', 'is_real_estate': 'immobilier', 'is_agrobusiness': 'agrobusiness', 'is_restoration': 'restauration', 'is_investment': 'investissement', 'is_general_commerce': r'commerce g.n.ral', 'is_BTP': r'travaux [a-z]+ b.timent'}

email_pattern = r'[a-zA-Z0-9]+[-._]*[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.[a-z]{2,}'
phone_number_pattern = r'([0-9]{8,13})|(\d{2} \d{2} \d{2} \d{2})'
manager_pattern = re.compile(r'\b(mademoiselle|monsieur)\b [a-zA-Z]+( [a-zA-Z]+)*', re.IGNORECASE)

p_list = main_page.find_all('p')
for p in p_list:
    for expr in [r'\Adenomination', r'\Asiege social', r'\Ageranc']:
        res = re.search(expr, p.get_text().lower())
        if res != None:
            company[expr[2:]] = res.string.split(':')[1]
            continue

company["name"] = str(company["denomination"]).replace('«', '').replace('»', '').strip()

company["capital"] = re.search(r'\d+[.]*[ ]*\d{3}[.]*[ ]*\d{3}', main_page.getText()).group().replace(' ', '').replace('.', '')

company['manager'] = re.search(manager_pattern, company['geranc']).group().upper()

if re.search('[lom]|[togo]', company['siege social']) != None:
    company["is_national"] = True
else:
    company["is_national"] = False

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
    company['phone_number'] = '-'

emails = set(re.findall(email_pattern, main_page.get_text()))
if emails != set():
    company['email'] = [v for v in emails][0]
else:
    company['email'] = '-'

for (k,v) in sector.items():
    if re.search(v, main_page.get_text().lower()) != None:
        company[k] = True
    else:
        company[k] = False

company.pop('denomination')
company.pop('siege social')
company.pop('geranc')
for (k,v) in company.items():
    print(k, '->', v)

with open("company.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=company.keys())
    writer.writeheader()
    writer.writerows([company])