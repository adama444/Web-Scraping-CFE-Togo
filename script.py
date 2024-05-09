import requests
from bs4 import BeautifulSoup
import re
import csv

url = 'https://cfetogo.tg/annonces-legales/details-annonce-152.html'
response = requests.get(url)

if response.status_code != 200:
    print('Not Found')
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
main_page = soup.find_all('div', {'class': 'col-md-12'})[1]

company = {}

if re.search(re.compile('constitution de societe', re.IGNORECASE), main_page.get_text()) != None:
    sector = {'is_import_export': r'import[ ]*-[ ]*export', 'is_transport': 'transport', 'is_real_estate': 'immobili.r', 'is_agrobusiness': 'agrobusiness', 'is_restoration': 'restauration', 'is_investment': 'investissement', 'is_general_commerce': r'commerce g.n.ral', 'is_BTP': r'b.timent|travaux public'}

    email_pattern = r'[a-zA-Z0-9]+[-._]*[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.[a-z]{2,}'
    phone_number_pattern = r'([0-9]{8,13})|(\d{2} \d{2} \d{2} \d{2})'
    manager_pattern = re.compile(r'\b(mademoiselle|monsieur|madame)\b \w+([ ]*-*\w+){,2}', re.IGNORECASE)
    capital_pattern = r'\d+[.]*[ ]*\d{3}[.]*[ ]*\d{3}'

    p_list = main_page.find_all('p')
    if p_list:
        for p in p_list:
            for expr in [r'\Adenomination', r'\Asiege social', r'\Ageranc', r'\Aadministration']:
                res = re.search(expr, p.get_text().lower())
                if res != None and res.string.find(':') != -1:
                    company[expr[2:]] = res.string.split(':')[1].strip()
                    continue
    else:
        print('Bad page HTML format')
        exit()
    
    if 'denomination' in company:
        company["name"] = str(company["denomination"]).replace('«', '').replace('»', '')
    else:
        company['name'] = '-'

    if re.search(capital_pattern, main_page.get_text()) != None:
        company["capital"] = re.search(capital_pattern, main_page.get_text()).group().replace(' ', '').replace('.', '')
    else:
        company['capital'] = 'moins de 1.000.000'

    if 'geranc' in company and re.search(manager_pattern, company['geranc']) != None:
        company['manager'] = re.search(manager_pattern, company['geranc']).group().upper()
    else:
        if 'administration' in company and re.search(manager_pattern, company['administration']) != None:
            company['manager'] = re.search(manager_pattern, company['administration']).group().upper()
        else:
            company['manager'] = '-'
    if 'siege social' in company:
        if re.search('[lom]|[togo]', company['siege social']) != None:
            company["is_national"] = True
        else:
            company["is_national"] = False
    else:
        company['is_national'] = True

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

    if 'denomination' in company:
        company.pop('denomination')

    if 'siege social' in company:
        company.pop('siege social')

    if 'geranc' in company:
        company.pop('geranc')
    else:
        if 'administration' in company:
            company.pop('administration')

for (k,v) in company.items():
    print(k, '->', v)

#with open("./company.csv", "w") as csvfile:
#    writer = csv.DictWriter(csvfile, fieldnames=company.keys())
#    writer.writeheader()
#    writer.writerows([company])