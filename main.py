import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=28.09.2021'

source = requests.get(url)
main_text = source.text

soup = BeautifulSoup(main_text, features="html.parser")

table = soup.find('table', {'class': 'data'})
tr = soup.findAll('tr')
th = soup.findAll('th')

all_line = []
for line in tr:
        all_line.append(line.text.splitlines()[1:])

df_main = pd.DataFrame(all_line)
df_main.index = df_main[3]
df_main.columns = df_main.iloc[0]
df_main = df_main.drop(df_main.index[0])
df_main = df_main.drop('Валюта', 1)


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(df_main)