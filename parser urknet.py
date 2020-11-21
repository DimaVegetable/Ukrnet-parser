import requests
import json
import datetime
from bs4 import BeautifulSoup
from pathlib import Path

CountDays = int(input())
now = datetime.datetime.now()
startDate = now.replace(tzinfo=datetime.timezone.utc).timestamp()
endDate = startDate - CountDays * 86400


def Get_list_News(URL):
    resultArr = []
    FlagIsDateCorrect = True
    page = 1
    while (FlagIsDateCorrect):
        thisPageUrl = URL + str(page) + '/'
        response = requests.get(thisPageUrl)
        a = json.loads(response.text)
        if "tops" in a:
            NewsByPage = a['tops']
        else:
            NewsByPage = a['cluster']['News']

        if len(NewsByPage) < 80:
            break
        for News in NewsByPage:
            if News['DateCreated'] < endDate:
                FlagIsDateCorrect = False
            else:
                resultArr.append(News)
        page += 1
    return resultArr


newsList = Get_list_News('https://www.ukr.net/news/dat/main/')


def Get_News(newsList):
    news1 = []

    for item in newsList:
        if 'News' in item:
            news1 += Get_list_News(
                'https://www.ukr.net/news/dat/main/' + str(item['SeoTitle']) + "/" + str(item['Id']) + "/1/")
        else:
            news1.append(item)

    return news1


def Parser(newsList):
    Path('D:\\test').mkdir(parents=True, exist_ok=True)
    Path('D:\\test\\test_title').mkdir(parents=True, exist_ok=True)
    Path("D:\\test\\test_content").mkdir(parents=True, exist_ok=True)
    File1 = open('D:\\test\\test_title\\test.txt', 'w')
    for news in newsList:
        try:
            File1.write('id: ' + str(news['Id']))
            File1.write('\ntitle: ' + news['Title'])
            File1.write('\nurl: ' + news['Url'] + '\n\n')

            response = requests.get(news['Url'])
            soup = BeautifulSoup(response.text, 'html.parser')
            File = open('D:\\test\\test_content\\' + str(news['Id']) + '.txt', 'w', encoding='utf-8')
            for p in soup.find_all('p'):
                File.write(p.get_text() + '\n')

            File.close()
        except Exception as e:
            print('Exception: ', news['Url'], str(e))
            try:
                response = requests.get(news['Url'])
                soup = BeautifulSoup(response.text, 'html.parser')
                File = open('D:\\test\\test_content\\' + str(news['Id']) + '.txt', 'w', encoding='utf-8')
                for p in soup.find_all('p' + '\n'):
                    File.write(p.get_text())

                File.close()
            except Exception as e:
                print('Exception: ', news['Url'], str(e))
    File1.close()


if __name__ == '__main__':
    news = Get_News(newsList)
    Parser(news)
