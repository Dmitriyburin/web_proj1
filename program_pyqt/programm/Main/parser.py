import requests
from bs4 import BeautifulSoup

url = 'https://olimpiada.ru/activities?type=any&subject%5B7%5D=on&class=any&period_date=&period=year'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
olympiads = soup.find_all('div', class_='fav_olimp olimpiada')

for i, olymp in enumerate(olympiads):
    title_olymp = olymp.find('span', class_='headline').text
    print(f'{i} - {title_olymp}')
