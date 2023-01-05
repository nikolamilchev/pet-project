import Form as design
from PyQt5 import QtWidgets

from PyQt5 import QtCore
import sys

import time
import json
import re

import requests
import ast
from bs4 import BeautifulSoup
from threading import Thread,currentThread


def magnit_parser():
    def fetch(url,params):
        auto_ru_responce = requests.post(url=url,headers=params['headers'],data=params['body'])
        return auto_ru_responce
    t = currentThread()
    i = 1
    while getattr(t, "do_run", True):
        rs = fetch("https://magnit.ru/promo/", {
              "headers": {
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "cookie": "",
            "Referer": "https://magnit.ru/",
            "Referrer-Policy": "origin",
            'User-Agent': ''
          },
          "body": f'page={i}',
          "method": "POST"
        })

        #print(f'request number: {i},status_code: {rs.status_code}, len: {len(rs.text)}')
        if len(rs.text)==0:
            print('end of product')
            time.sleep(3600)
            i=0
        else:
            soup = BeautifulSoup(rs.text, "html.parser")
            for price in soup.find_all('div',class_='label__price label__price_new'):
                if len(price.find_all('span',class_='label__price-decimal'))+len(price.find_all('span',class_='label__price-integer'))==2:
                    name = price.parent.parent.parent.find_all('div',class_='card-sale__title')[0].text
                    name = re.sub(r'[^а-яА-ЯёЁa-zA-Z0-9 ]','',name)
                    count_ = int(price.find_all('span',class_='label__price-integer')[0].text)+0.01*int(price.find_all('span',class_='label__price-decimal')[0].text)
                    with open('data.json','r', encoding='utf-8') as f:
                        lst_ = json.load(f)
                    if name not in lst_["magnit"].keys():
                            lst_["magnit"][name] = []
                    if len(lst_["magnit"][name])==0 or lst_["magnit"][name][-1]!=count_:
                        lst_["magnit"][name].append(count_)
                    l_ = re.sub('\"','',str(lst_))
                    l_ = re.sub('\'','\"',l_)
                    with open('data.json','w', encoding='utf-8') as f:
                        f.write(l_)
            #print('data written')
            i+=1
         
class Bot_Form(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        self.close_button.clicked.connect(self.close)
        self.cache_button.clicked.connect(self.clean_json)
        self.start_button.clicked.connect(self.start_bot)
        self.stop_button.clicked.connect(self.stop_bot)
        self.find_button.clicked.connect(self.show_result)
        self.magnit_parser_ = None
        
    def show_result(self):
        def mini_plots(data_x,data_y):
            self.plot.clear()
            self.plot.setBackground('w')
            self.plot.plot(data_x, data_y)
            self.plot.showGrid(x=True, y=True)
        name = self.find_edit.text()
        with open('data.json','r', encoding='utf-8') as f:
            lst_ = json.load(f)
        for market in lst_.keys():
            if name not in lst_[market].keys():
                self.count_edit.setText('нет продукта')
            else:
                list_of_price = lst_[market][name]
        x = range(len(list_of_price))
        y = list_of_price
        last_price = list_of_price[-1]
        self.count_edit.setText(str(last_price))
        mini_plots(x,y)
    def clean_json(self):
        with open('data.json','r', encoding='utf-8') as f:
            lst_ = json.load(f)
        keys = lst_.keys()
        dict_ = {"magnit" : {}}
        l_ = re.sub('\'','\"',str(dict_))
        with open('data.json','w', encoding='utf-8') as f:
            f.write(l_)
    def start_bot(self):
        self.magnit_parser_ = Thread(target=magnit_parser)
        self.magnit_parser_.start()
    def stop_bot(self):
        self.magnit_parser_.do_run=False
        
       
       
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Bot_Form()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()