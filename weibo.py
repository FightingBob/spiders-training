import requests
from fake_useragent import UserAgent
from pyquery import PyQuery
from urllib.parse import urlencode
from requests.packages import urllib3
from pymongo import MongoClient

# 关闭警告
urllib3.disable_warnings()

base_url = 'https://m.weibo.cn/api/container/getIndex?'

# 激活本地MongoDB客户端
client = MongoClient('localhost',27001)
# 创建数据库
pages = client['pages']
# 创建集合
ma_yun = pages['ma_yun']

# 保存到mongoDB中
def save_to_mongo(result):
    if ma_yun.insert_one(result):
        print('saved to Mongo','已获取{number}条数据'.format(number=ma_yun.count()))

# 生成UA
def create_user_agent():
    ua = UserAgent(use_cache_server=False)
    # print(ua.chrome)
    return ua.chrome

# 生成headers
def create_headers():
    headers = {
        'User-Agent': create_user_agent()
    }
    return headers

# 获取页面
def get_page(page):
    # 设置参数
    params = {
        'sudaref':'germey.gitbooks.io',
        'display':'0',
        'retcode':'6102',
        'type':'uid',
        'value':'2145291155',
        'containerid':'1076032145291155',
        'page':page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url,create_headers(),verify=False)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)

# 解析页面
def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        if items != None:
            for item in items:
                item = item.get('mblog')
                weibo = {}
                weibo['id'] = item.get('id')
                # 将正文中的 HTML 标签去除掉
                weibo['text'] = PyQuery(item.get('text')).text()
                # 点赞数
                weibo['attitudes_count'] = item.get('attitudes_count')
                # 评论数
                weibo['comments_count'] = item.get('comments_count')
                # 发布时间
                weibo['datetime'] = item.get('created_at')
                # 转发数
                weibo['reposts_count'] = item.get('reposts_count')

                yield weibo

# 设置主方法进行调用其他方法
def main():
    for page in range(1,30):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            save_to_mongo(result)

if __name__ == '__main__':
    main()

