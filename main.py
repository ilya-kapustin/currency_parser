import requests
from bs4 import BeautifulSoup

print('Введите дату в формате хх.хх.ххх (28.09.2021)')
date = input('Дата ')
url = f'httpswww.cbr.rucurrency_basedailyUniDbQuery.Posted=True&UniDbQuery.To={date}'

source = requests.get(url)
main_text = source.text
soup = BeautifulSoup(main_text, features='html.parser')

table = soup.find('table', {'class' 'data'})
tr = table.findAll('tr')

for line in tr[1]:
    print(line.text)

for line in tr[1]:
    print(line.text.splitlines()[1])
