import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
import time
import random
import bs4


class AnjukeSpider(object):
    def __init__(self):
        self.url = 'https://beijing.anjuke.com/community/fengtai/p{}/'

    def get_headers(self):
        ua = UserAgent()
        headers = {
            "accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie":
            "aQQ_ajkguid=534DDCC9-5DBA-263A-CF4D-SX0716083828; isp=true; 58tj_uuid=e559fdad-fdb9-4a73-8c60-9e6e3bf82987; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1563237510; als=0; _ga=GA1.2.1881437242.1569052175; ctid=30; wmda_uuid=edd62dcc1e73bddc16beeb56087fd1f8; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; sessid=F6826357-F68F-1E17-B5A1-99FEA17341CA; lps=http%3A%2F%2Fwww.anjuke.com%2F%7Chttps%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DcuNIKoO-jX3CGzD7komT_lY2umPIHgZjjBdMMdFnpZHirHVPOLorVTafN32HS5R_%26ck%3D7150.2.84.414.190.439.289.917%26shh%3Dwww.baidu.com%26sht%3D02003390_42_hao_pg%26wd%3D%26eqid%3Dc2951ba5003c81ad000000065d881f86; twe=2; wmda_session_id_6289197098934=1569202063874-b62b0050-2be7-3851; _gid=GA1.2.388348263.1569202065; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DcuNIKoO-jX3CGzD7komT_lY2umPIHgZjjBdMMdFnpZHirHVPOLorVTafN32HS5R_%2526ck%253D7150.2.84.414.190.439.289.917%2526shh%253Dwww.baidu.com%2526sht%253D02003390_42_hao_pg%2526wd%253D%2526eqid%253Dc2951ba5003c81ad000000065d881f86; new_uv=3; new_session=0",
            "referer": "https://beijing.anjuke.com/community/?from=navigation",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": ua.random
        }
        return headers

    def get_link(self, url):
        r = requests.get(url=url, headers=self.get_headers())
        r.encodeing = 'utf-8'
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        link = []
        for aTag in soup.find_all('h3'):
            aTag = aTag.find('a')
            if isinstance(aTag, bs4.element.Tag):
                link.append(aTag.attrs['href'])
        price = []
        for i in soup.find_all('strong'):
            price.append(i.string)
        # print(link)
        # print(price)
        # for i in zip(link, price):
        # print(i)
        return zip(link, price)

    def parse_message(self, url, price):
        dict_result = {
            '小区': '-',
            '价格': '-',
            '物业类型：': '-',
            '物业费：': '-',
            '总建面积：': '-',
            '总户数：': '-',
            '建造年代：': '-',
            '停车位：': '-',
            '容积率：': '-',
            '绿化率：': '-',
            '开发商：': '-',
            '物业公司：': '-',
            '相关学校：': '-',
            '所属商圈：': '-'
        }

        r = requests.get(url=url, headers=self.get_headers())
        r.encodeing = 'utf-8'
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        table1 = []
        _table1 = soup.find('div', attrs={"class": 'comm-title'})
        _table1 = _table1.find('h1')  # 提取小区名和地址
        table1.append(_table1.next)
        dict_result['小区'] = table1[0].replace('\t', '').replace('\n', '')
        dict_result['价格'] = price
        # 爬取第二阶段的数据
        _table2 = soup.find('dl', attrs={"class": 'basic-parms-mod'})
        j = []
        for dt in _table2.find_all('dt'):
            j.append((dt.string).replace('\xa0', ''))
        i = 0
        for dd in (_table2.find_all('dd')):
            dict_result[j[i]] = dd.string.replace('\t',
                                                  '').replace('\n',
                                                              '').split('(')[0]
            i = i + 1
        '''for (dd, dt) in (_table2.find_all('dd'), j):
            dict_result[dt] = dd.string   为啥不行？？？'''
        dict_result.pop('物业费：')
        dict_result.pop('物业类型：')
        dict_result.pop('建造年代：')
        dict_result.pop('开发商：')
        dict_result.pop('物业公司：')
        dict_result.pop('相关学校：')
        dict_result.pop('所属商圈：')
        print(dict_result)
        return dict_result

    def save_csv(self, result):
        headers = {'小区', '价格', '总建面积：', '总户数：', '停车位：', '容积率：', '绿化率：'}
        with open('北京丰台.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            # writer.writeheader()
            for row in result:
                writer.writerow(row)

    def run(self):
        C = 1
        for i in range(1, 40):  # 总的页
            url = self.url.format(i)
            link = self.get_link(url)
            list_result = []
            for j in link:
                try:
                    result = self.parse_message(j[0], j[1])
                    time.sleep(round(random.randint(3, 4), C))
                    list_result.append(result)
                except Exception as err:
                    print(err)
            self.save_csv(list_result)
            print("第%s页储存成功" % i)

        # url = 'https://qd.anjuke.com/community/view/875393?from=Filter_1&hfilter=filterlist'
        # self.parse_message(url)
        # self.get_link()


if __name__ == '__main__':
    spider = AnjukeSpider()
    spider.run()
