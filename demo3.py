from bs4 import BeautifulSoup
import requests
url_prefix = 'https://knewone.com/discover?page='
infos = []

# 获取单个页面数据
def getAPage(url,data = None):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    # print(soup)

    images = soup.select('header > a > img')
    titles = soup.select('section > h4 > a')
    links = soup.select('a.cover-inner')
    likes = soup.select('span.fanciers_count')

    if data == None:
        for image,title,link,like in zip(images,titles,links,likes):
            data = {
                'image':image.get('src'),
                'title':title.get_text(),
                'link':'https://knewone.com' + link.get('href'),
                'like':int(like.get_text())
            }
            print(data)

            infos.append(data)
# 获取多个加载的数据
def getMorePages(start,end):
    for url_suffix in range(start,end):
        getAPage(url_prefix + str(url_suffix))
        print('---------------已经获取{}条数据---------------'.format(len(infos)), sep='\n')
# 获取点赞排名前几的数据
def getInfosByLikes(order,infos =infos):
    infos = sorted(infos,key= lambda info:info['like'],reverse = True)
    for info in infos[:order]:
        print(info['like'],info['title'],info['image'],info['link'])

getMorePages(1,4)


getInfosByLikes(5)