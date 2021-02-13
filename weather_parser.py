import requests
from bs4 import BeautifulSoup

class Weather:

    def __init__(self, country, town):
        self.url = "https://world-weather.ru/pogoda/" + country + "/" + town + "/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.41 YaBrowser/21.2.0.1097 Yowser/2.5 Safari/537.36'}
        self.full_page = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(self.full_page.content, 'html.parser')

    def get_temp(self):
        convert = self.soup.findAll("div", {"id": "weather-now-number"})
        return convert[0].text

    def get_desc(self):
        convert = self.soup.findAll("span", {"id": "weather-now-icon"})
        #Проходим по тегу и вытаскиваем значение title
        for i in convert:
            title = i.attrs["title"]
        return title

    def get_feels(self):
        convert = self.soup.find(text='Ощущается').findNext('dd')
        return convert.text

    def get_pressure(self):
        convert = self.soup.find(text='Давление').findNext('dd')
        return convert.text

    def get_wind(self):
        convert = self.soup.find(text='Ветер').findNext('dd')
        return convert.text

    def get_humidity(self):
        convert = self.soup.find(text='Влажность').findNext('dd')
        return convert.text

