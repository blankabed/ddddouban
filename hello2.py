import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import pymongo
import pymysql

dict={
    "id":"",
    "图片链接":"",
    "电影名":"",
    "主演导演":"",
    "评分":"",
    "影片详细链接":""
}
def get_html(url):
    try:
        response=requests.get(url,allow_redirects=False)
        if response.status_code==200:
            html = response.text.encode(response.encoding).decode('utf-8', 'ignore')
            return html
        if response.status_code==302:
            print('302')
    except ConnectionError:
        return get_html(url)
def get_info():
    html = get_html("https://movie.douban.com/top250")
    soup=BeautifulSoup(html,"lxml")
    info1=soup.find_all('div', {'class': "hd"})
    info2=soup.find_all('p', {'class': ""})
    print(str(info2[0]).replace("\n",""))
    info4=soup.find_all('img',{'class': ""})
    info3 = soup.find_all('div', {'class': "star"})
    for i in range(0,25):
        dict["id"]=i+1
        dict["图片链接"]=re.findall(r'alt=".*?" class="" src="(.*?)" width=".*?"',str(info4[i]))[0]
        dict["电影名"]=re.findall(r'<span class="title">(.*?)</span>', str(info1[i]))[0]
        dict["类型"]=re.findall(r'^<p class="">.*?<br/>.*?/.*?/(.*?)</p>$',str(info2[i]).replace("\n",""))
        dict["影片详细链接"]=re.findall(r'<a class="" href="(.*?)">',str(info1[i]))
        dict["评分"]=re.findall(r'<span class="rating_num" property="v:average">(.*?)</span>'
                              ,str(info3[i]))
        dict["主演导演"]=re.findall(r'^<p class="">\s+(.*?)<br/>',str(info2[i]).replace("\n",""))
        bb=str(dict["主演导演"]).replace('xa0',"").replace("\\","").replace(" ","")
        dict["主演导演"]=bb
        aa=str(dict["类型"]).replace('xa0',"").replace("\\","").replace(" ","")
        dict["类型"] =aa

        save_mysqlinfo()
def save_info():
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn.moviedb
    my_set = db.test_set
    my_set.insert({ '电影名': dict['电影名'], '主演导演': dict['主演导演'],
                   '评分': dict['评分']})

def save_mysqlinfo():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='admin',
        db='douban',
    )
    cur = conn.cursor()

    # 插入一条数据
    sql = "INSERT INTO `douban_movie`(id,moviename,actoranddirector,grade,movieimg,movieurl,type) values (%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(sql,[dict["id"],dict['电影名'],str(dict["主演导演"]).replace('[',' ').replace(']',' '),str(dict["评分"]).replace('[',' ').replace(']',' '),str(dict["图片链接"]),str(dict["影片详细链接"]).replace('[',' ').replace(']',' ').replace("'",''),str(dict["类型"]).replace('[',' ').replace(']',' ').replace("'",'')])
    conn.commit()
    cur.close()
    conn.close()

get_info()


