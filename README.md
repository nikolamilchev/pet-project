# pet-project
Здесь исходный код парсера магнита.
Тему выбрал так как постоялся интересовался как изменяются цены в магните.
Задача выполнена с помощью request(отправляет специальный запрос и забирает html Yразметку сайта(запрос отправляется несколько раз чтобы прочитать все товары, в среднем отправляется 200 запросов).
Изначально хотел сам распарсить полученную html, но оказалось слишком тяжело и использовал BeathifulSoup.
бот работает в отдельном потоке так что можно сразу смотреть на результаты которые сохраняются в json.
Не стал брать имитаторы браузеров(типа Selenium) так как мне не нравится подобный подход. 
Хотел взять дополнительно данные с КБ но у них весьма хитрый сайт и тяжело слать Get-запрос(они используют MD5) за зимние праздники удалось только один раз получить данные, притом следующий запрос опять принёс пустышку.
Список использованных библиотек лежит в файле requirement.txt
Исполняемый файл называется Form_result.py( хоть и удалось конвертировать проект в .exe файл он оказался слишком тяжелым чтобы быть залитым на гит)
