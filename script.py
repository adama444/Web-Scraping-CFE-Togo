import requests
from bs4 import BeautifulSoup
import re

url = 'https://cfetogo.tg/annonces-legales/details-annonce-1.html'
response = requests.get(url)

company = {}

soup = BeautifulSoup(response.content, 'html.parser')
main_page = soup.find('div', {'class': 'main'})

#company_title = main_page.find_all('p')[2]
#company['name'] = company_title.text

p_list = main_page.find_all('p')
for p in p_list:
    for expr in [r'\ADENOMINATION', r'\AOBJET SOCIAL', r'\ACAPITAL SOCIAL', r'\ASIEGE SOCIAL', r'\ADUREE', r'\AGERANCE']:
        res = re.search(expr, p.text)
        if res != None:
            company[expr[2:]] = res.string.split(':')[1]
            continue

#for (k,v) in company.items():
#    print(k, '->', v)

print(company["DENOMINATION"])