from urllib import request
from bs4 import BeautifulSoup
import chardet
import json

if __name__ == "__main__":
    # url = "http://www.baidu.com"
    url = "http://www.ziroom.com/z/vr/61861486.html"
    head = {}
    head['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    req = request.Request(url,headers=head)
    response = request.urlopen(req)
    html = response.read()
    charset = chardet.detect(html).get('encoding')
    html = html.decode(charset)
    # print(html)
    soup = BeautifulSoup(html,'lxml')
    # print(soup.prettify()+"\n")
    divs = soup.find("input",id="house_id")
    print(divs)
    house_id = divs['value']
    print(house_id)

    url2 = "http://www.ziroom.com/detail/info?id=61861486&house_id="+house_id
    req2 = request.Request(url2,headers=head)
    resp2 = request.urlopen(req2)
    jsonstr = resp2.read()
    json = json.loads(jsonstr,encoding="utf-8")
    print(json)
    print(json['data']['air_part']['air_quality']['show_info']['status'])
    print(json['data']['air_part']['vanancy']['status'])

