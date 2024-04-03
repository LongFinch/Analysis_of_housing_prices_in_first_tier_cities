import requests
import json
import re
import random

from lxml import html


class reptile:
    # 需要爬取城市的名字
    citys = ['北京', '上海', '广州', '深圳', '惠州']
    city_urls = {"北京": "bj", "上海": "sh", "广州": "gz", "深圳": "sz", "惠州": "hui"}
    # 用于匹对户型和朝向的正则式
    numeric_pattern = re.compile(r'\b(?<!室|厅|卫)\d+(\.\d+)?\b')
    direction_pattern = re.compile(r'东|南|西|北')
    room_pattern = re.compile(r'(\d+房间)?(\d+室)?(\d+厅)?\d+卫')

    def url_construction(self):
        for city in self.citys:
            c_url = self.city_urls[city]
            district_urls = self.get_district_urls(c_url)
            for district_url in district_urls:
                # 获取每个地点的域名url
                location_urls = self.get_locations_url('http://' + c_url + '.lianjia.com' + district_url)
                for location_url in location_urls:
                    # 获取每个网页的页数
                    pg_num = self.get_pg_num('http://' + c_url + '.lianjia.com' + location_url)
                    if pg_num:
                        # random_number = str(random.randint(1, 2))
                        for num in range(pg_num):
                            url = 'http://' + c_url + '.lianjia.com' + location_url + 'pg' + str(num)
                            self.web_scraper(url, c_url)


    def get_district_urls(self, c_url):
        url = 'https://' + c_url + '.lianjia.com/zufang/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.150 Safari/537.36"
        }  # 添加headers，模拟浏览器请求
        response = requests.get(url, headers=headers)  # 发送GET请求
        urls = []  # 初始化urls为空列表
        if response.status_code == 200:
            # 使用lxml解析HTML内容
            tree = html.fromstring(response.content)
            with open("temp.txt",'w',encoding='utf-8')as f:
                f.write(response.text)
            # 使用XPath表达式提取所需的信息
            urls = tree.xpath("//li[@data-type='district'][position()>1]/a/@href")
        return urls

    # 获取所有板块链接
    def get_locations_url(self, district_url):
        locations = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.150 Safari/537.36"
        }  # 添加headers，模拟浏览器请求
        response = requests.get(district_url,headers=headers)
        if response.status_code == 200:
            # 使用lxml解析HTML内容
            tree = html.fromstring(response.content)
            # 使用XPath表达式提取所需的信息
            locations = tree.xpath("//li[@data-type = 'bizcircle'][position()>1]/a/@href")
        return locations

    def get_pg_num(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.150 Safari/537.36"
        }  # 添加headers，模拟浏览器请求
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            # 使用lxml解析HTML内容
            tree = html.fromstring(response.content)

            # 使用XPath表达式提取所需的信息
            page_num = tree.xpath("//*[@id='content']/div[1]/div[@class='content__pg']/@data-totalpage")
            page_num = int(page_num[0]) if page_num else None
        return page_num

    def web_scraper(self, url, c_url):
        item = {
            # 需要爬取的内容有名字,地区，总价，面积，单价，朝向,户型
            'name': "",
            'district': "",
            'total_price': "",
            'area': [],
            'direction': "",
            'layout': ""
        }
        # 发送GET请求获取网页内容
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.150 Safari/537.36"
        }  # 添加headers，模拟浏览器请求
        '''

        headers_list = [
            {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666'
            }, {
                'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320'
            }, {
                'user-agent': 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+'
            }, {
                'user-agent': 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G965U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SM-T837A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 550) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 6P Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)'
            }, {
                'user-agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 3 Build/PQ1A.181105.017.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
            }, {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            }, {
                'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
            }
        ]

        # 避免被发现是爬虫程序
        try:
            response = requests.get(url, headers=random.choice(headers_list),
                                    timeout=1)  # 超时设置为3秒
        except:
            for i in range(4):  # 循环去请求网站
                response = requests.get(url, headers=random.choice(headers_list),
                                        timeout=3)
                if response.status_code == 200:
                    break

        # 检查请求是否成功
        if response.status_code == 200:
            # 使用lxml解析HTML内容
            tree = html.fromstring(response.content)

            for each in tree.xpath("//*[@id='content']/div[1]/div[1]/div"):

                # 使用XPath表达式提取所需的信息
                item['name'] = each.xpath(
                    "./div/p[1]/a/text()")[0].strip()

                district_list = each.xpath(
                    "./div/p[2]/a[2]/text()")  #
                item['district'] = district_list[0] if district_list else None

                item['total_price'] = each.xpath(
                    "./div/span/em/text()")[0]

                information = each.xpath(
                    "./div/p[2]/text()")  # 列表取第一个元素即字符串信息

                # 独栋数据存在一些面积是一个范围的，用list先存着
                item['area'] = [match.group() for match in
                                self.numeric_pattern.finditer(''.join(information))]

                item['direction'] = ''.join(self.direction_pattern.findall(
                    ''.join(information)))

                room_info = next((entry for entry in information if
                                  self.room_pattern.search(entry)), None)
                if room_info:
                    item['layout'] = self.room_pattern.search(room_info).group()

                if (item['name'] and item['district'] and item[
                    'total_price'] and
                        item['area'] and item['direction']
                        and item['layout']):  # 独栋户型会缺失数据
                        # 将数据写入json文件中
                        with open(c_url + '_data.json', 'a',
                                  encoding='utf-8') as json_file:
                            json.dump(item, json_file, ensure_ascii=False)
                            json_file.write('\n')  # 换行，确保每个字典占一行
        else:
            # 打印错误信息并返回空列表或其他适当的值
            print(f"Failed to fetch {url}. Status code: {response.status_code}")


a = reptile()
a.url_construction()
