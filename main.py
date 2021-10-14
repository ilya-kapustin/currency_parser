from datetime import datetime, timedelta
import pandas as pd
import requests
from bs4 import BeautifulSoup


class AllCurrency:
    def __init__(self, start_date, finished_date, save_name):
        self.all_line = []
        self.url = 'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To='
        self.start_date = start_date
        self.url_now = None
        self.save_name = save_name
        self.finished_date = finished_date

    def settings_views(self):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

    def settings_date(self, date):
        date = datetime.strptime(date, '%d.%m.%Y')
        return date

    def settings_url(self, url):
        source = requests.get(url)
        main_text = source.text
        soup = BeautifulSoup(main_text, features="html.parser")
        table = soup.find('table', {'class': 'data'})
        self.tr = soup.findAll('tr')

    def run(self):
        self.settings_views()

        self.url_now = self.url + self.start_date
        self.settings_url(self.url_now)
        print(self.url_now)

        self.start_date = self.settings_date(date=self.start_date)
        self.finished_date = self.settings_date(date=self.finished_date)

        for line in self.tr[:1]:
            self.all_line.append(line.text.splitlines()[1:])
        self.all_line[0].append('Дата')

        while True:
            self.start_date = self.start_date + timedelta(days=1)
            self.start_date = self.start_date.strftime("%d.%m.%Y")
            self.url_now = self.url + self.start_date
            self.settings_url(self.url_now)
            print(self.url_now)
            self.start_date = self.settings_date(date=self.start_date)
            for line in self.tr[1:]:
                if '<td>Украинских карбованецев</td>' not in str(line):
                    self.all_line.append(line.text.splitlines()[1:])
                    self.all_line[-1].append(self.start_date.strftime("%d.%m.%Y"))
            if str(self.finished_date) == str(self.start_date):
                break
        self.clean_data()

    def clean_data(self):
        data = pd.DataFrame(self.all_line)
        # data.index = data['Цифр. код']
        data.columns = data.iloc[0]
        data = data.drop(data.index[0])
        # data = data.drop('Валюта', axis=1)
        data.to_csv(self.save_name, encoding='utf-8')
        print(data)


if __name__ == '__main__':
    AllCurrency('01.07.1992', '10.07.1992', 'data').run()
