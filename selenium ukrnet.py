import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path

browser = webdriver.Chrome("C:\chromedriver.exe")
browser.get('https://www.ukr.net/news/main.html')

html = browser.page_source

soup = BeautifulSoup(html, 'html.parser')

ukr_net_links = []
else_net_links = []


def get_links():
    global ukr_net_links, else_net_links
    link = soup.find_all('div', class_='im-tl')
    for links in link:
        result = links.contents[1]['href']
        if result.startswith('//'):
            result_else = 'https:' + result
            ukr_net_links.append(result_else)
        else:
            else_net_links.append(result)


def get_new_links(ukr_net_links, else_net_links):
    for linkss in ukr_net_links:
        browser.get(linkss)
        html_next = browser.page_source
        soup_next = BeautifulSoup(html_next, 'html.parser')
        link_next = soup_next.find_all('div', class_='im-tl')
        for links in link_next:
            r = links.contents[1]['href']
            else_net_links.append(r)


Path("D:\\test_selenium").mkdir(parents=True, exist_ok=True)


def parser(else_net_links):
    for i in else_net_links:
        response = requests.get(i)
        soup1 = BeautifulSoup(response.text, "html.parser")
        File = open('D:\\test_selenium\\' + soup['Id'] + '.txt', 'w', encoding='utf-8')
        for p in soup1.find_all('p'):
            File.write(p.get_text() + '\n')
        File.close()
        break


if __name__ == '__main__':
    get_links()
    # print(ukr_net_links)
    # print(len(ukr_net_links))
    # print(else_net_links)
    # print(len(else_net_links))
    get_new_links(ukr_net_links, else_net_links)
    # print(else_net_links)
    # print(len(else_net_links))
    parser(else_net_links)
