import requests
from bs4 import BeautifulSoup


def parse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    olympiads = soup.find_all('a', class_='black_hover_blue')[1:]
    subject_class = soup.find_all('span', class_='light_grey')

    return olympiads, subject_class


def get_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    count_page = soup.find('ul', {'id': 'counter'})
    for i, page in enumerate(count_page):
        if i == 5:
            return int(page.text)


def main():
    count_olymps = 0
    url = f'https://info.olimpiada.ru/activities/single/2022-01-10/sort/users_rate?region%5B78%5D=on&reg_inc=1&subject%5B3%5D=on&subject%5B11%5D=on&subject%5B10%5D=on&subject%5B7%5D=on&subject%5B25%5D=on&subject%5B8%5D=on&subject%5B6%5D=on&subject%5B16%5D=on&subject%5B1%5D=on&subject%5B12%5D=on&subject%5B19%5D=on&subject%5B13%5D=on&sub_inc=1region%5B78%5D=on&reg_inc=1&sub_inc=1/page/1'
    for i in range(1, get_page(url) + 1):
        olympiads, subject_class = parse(url)
        for j, olymp in enumerate(olympiads):
            print(f'{count_olymps} - {olymp.text} - {subject_class[j].text}')
            count_olymps += 1

        page = i
        url = f'https://info.olimpiada.ru/activities/single/2022-01-10/sort/users_rate?region%5B78%5D=on&reg_inc=1&subject%5B3%5D=on&subject%5B11%5D=on&subject%5B10%5D=on&subject%5B7%5D=on&subject%5B25%5D=on&subject%5B8%5D=on&subject%5B6%5D=on&subject%5B16%5D=on&subject%5B1%5D=on&subject%5B12%5D=on&subject%5B19%5D=on&subject%5B13%5D=on&sub_inc=1region%5B78%5D=on&reg_inc=1&sub_inc=1/page/{page}'


if __name__ == '__main__':
    main()
