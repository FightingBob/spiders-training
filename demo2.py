from bs4 import BeautifulSoup
import requests
import time
import re

# # 1. 设置网页地址
# url = 'http://www.mafengwo.cn/g/10720.html'
#
# # 2. 使用Request向服务器请求获取内容
# web_data = requests.get(url) # 将返回的response储存起来
# # 3. 用BeatifulSoup解析网页文本
# soup = BeautifulSoup(web_data.text,'lxml')
# # print(soup)
# images = soup.select('a[class="avatar48"] > img')
# names = soup.select('div.mod.group-leader > ul > li > p > a[target="_blank"]')
# # print(names)
# # print(view)
# infos = []
# for image,name in zip(images,names):
#     data = {
#         'image':image.get('src'),
#         'name':name.get_text()
#     }
#     infos.append(data)
# print(infos)
url = 'http://search.qyer.com/hotel/89580_4.html'
urls = ['http://search.qyer.com/hotel/89580_{}.html'.format(str(i)) for i in range(1,10)] # 最多157页
infos = []
# print(urls)

# 批量爬取数据
def getAUrl(urls):
    data_number = 0
    for url in urls:
        getAttractions(url)
        print('--------------{}-----------------'.format(len(infos)),sep='\n')

# 爬取当页面数据
def getAttractions(url,data = None):
    web_data = requests.get(url)
    time.sleep(2)
    soup = BeautifulSoup(web_data.text,'lxml')
    # print(soup)

    hotel_names = soup.select('ul.shHotelList.clearfix > li > h2 > a')
    hotel_images = soup.select('span[class="pic"] > a > img')
    hotel_points = soup.select('span[class="points"]')
    hotel_introduces = soup.select('p[class="comment"]')
    hotel_prices = soup.select('p[class="seemore"] > span > em')

    if data == None:
        for name,image,point,introduce,price in \
                zip(hotel_names,hotel_images,hotel_points,hotel_introduces,hotel_prices):
            data = {
                'name':name.get_text().replace('\r\n','').strip(),
                'image':image.get('src'),
                'point':re.findall(r'-?\d+\.?\d*e?-?\d*?', point.get_text())[0],
                'introduce':introduce.get_text().replace('\r\n','').strip(),
                'price':int(price.get_text())
            }
            # print(data)
            infos.append(data)

# 根据价格从高到低进行排序
def getInfosByPrice(infos = infos):
    infos = sorted(infos, key=lambda info: info['price'], reverse=True)
    for info in infos:
        print(info['price'], info['name'])

# getAttractions(url)

getAUrl(urls)

# getInfosByPrice()
