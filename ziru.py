import json, chardet, threading, time, sys, traceback
from urllib import request
from bs4 import BeautifulSoup

if __name__ == "__main__":
    house_pages = ["61742161", "61861486", "61864482", "61847013"]
    dingding_house_status = "已检测"
    i = 0
    while True:
        if i == house_pages.__len__():
            i = 0
        house_page = house_pages[i]
        i = i + 1
        dingding_msg = ""
        try:
            dingding_flag = False
            try:
                ziru_url = "http://www.ziroom.com/z/vr/" + house_page + ".html"
                print("\n房源page：" + ziru_url)
                dingding_msg += "房源page："+ziru_url
                ziru_head = {
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/70.0.3538.102 Safari/537.36"}
                ziru_req = request.Request(ziru_url, headers=ziru_head)
                ziru_response = request.urlopen(ziru_req)
                ziru_html = ziru_response.read()
                ziru_charset = chardet.detect(ziru_html).get('encoding')
                ziru_html = ziru_html.decode(ziru_charset)
                # print(html)
                ziru_soup = BeautifulSoup(ziru_html, 'lxml')
                # print(soup.prettify()+"\n")
                room_name = ziru_soup.find('div', class_="room_name").h2.get_text()
                room_name = room_name.strip()
                print("房源名称：" + room_name)
                dingding_msg += "\n房源名称："+room_name
                ziru_divs = ziru_soup.find("input", id="house_id")
                # print(divs)
                house_id = ziru_divs['value']
                print("房源id：" + house_id)
                dingding_msg += "\n房源id：" + house_id

                ziru_url2 = "http://www.ziroom.com/detail/info?id=" + house_page + "&house_id=" + house_id
                print("房源预定信息：" + ziru_url2)
                # dingding_msg += "\n房源预定信息：" + ziru_url2
                ziru_req2 = request.Request(ziru_url2, headers=ziru_head)
                ziru_resp2 = request.urlopen(ziru_req2)
                ziru_json = ziru_resp2.read()
                ziru_jsonStr = json.loads(ziru_json, encoding="utf-8")
                # print(jsonStr)
                air_status = ziru_jsonStr['data']['air_part']['air_quality']['show_info']['status']
                house_status = ziru_jsonStr['data']['air_part']['vanancy']['status']
                print("房源空检状态：" + air_status)
                dingding_msg += "\n房源空检状态：" + air_status
                if(dingding_house_status in air_status):
                    dingding_flag = True
                print("房源预定状态：" + house_status)
                dingding_msg += "\n房源预定状态：" + house_status

            except Exception as e:
                print("获取房源信息时出错,", e)

            if dingding_flag:
                dingding_req_json = {
                    'msgtype': 'text',
                    'text':
                        {
                            'content': dingding_msg
                        }
                }
                print(dingding_req_json)
                dingding_url = "https://oapi.dingtalk.com/robot/send?access_token" \
                               "=28d9d3aed06a365195128ddfab671bfbcf54529a321df4e054386b8591b5702c "
                dingding_header = {'Content-Type': 'application/json'}
                dingding_req = request.Request(dingding_url, data=json.dumps(dingding_req_json).encode('utf-8'),
                                               headers=dingding_header)
                dingding_resp = request.urlopen(dingding_req)
                dingding_result = dingding_resp.read()
                print(dingding_result)

            time.sleep(300)
        except Exception as e:
            print("程序执行出错，房源pageid：" + house_page + ",", e)
