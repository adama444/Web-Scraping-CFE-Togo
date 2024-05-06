import requests
from bs4 import BeautifulSoup

url = 'https://cfetogo.tg/annonces-legales/details-annonce-1.html'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

company_title = soup.find('div', {'class': 'main'}).find_all('p')[2]
print(company_title)