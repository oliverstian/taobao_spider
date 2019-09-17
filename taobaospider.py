# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request, FormRequest
from taobao.items import TaobaoItem
import re
import json


class TaobaospiderSpider(Spider):
    name = 'taobaospider'
    # allowed_domains = ['taobao.com']

    def __init__(self, *args, **kwargs):
        super(TaobaospiderSpider, self).__init__(*args, **kwargs)
        self.user_name = '13066882860'

        self.ua = "120#bX1bSBcMeep5a1dA11YDGQ+fbc82N7VZ1BVt1Lf0MJVf2mX2oiS0O0m11CJOxbAMN4RjIURckhZ4H/QleiHPJ/MVV4K2m0Eq1PK3N+RwFKBrbAiP/qJf3mhb+7phZ1Hud0aNXsuXzYK9lkTFeaAOe0qbYO8OXvVM8qeDha/QLJuEjQL8SX44nZ0EEeDCrysFYv7xHOdxdDOEq+mwJJ2JTbDSTLvAPXubnUldWqeqjvb575GPN0S/bI5S1JoPyY/Kb5vtNqe/aIbS7UGPWWl/bbwN3T+YuIGwc5pqb1G74JiugnfyXFJk2/j16WDbORsZzS7qDyhhmro6QcZ7CiujvG41DrVXl/Q/XEccEMtls28vo9dk1D0OzdFz40eF4G2wc7MKmnUHV05lqBCMUjtMyg0pbZkOUp05G8jSYO4V0FHWy8AuhhIAPWy46UtF2oAFGZjkj/6c0pyelhDujWAVtXywteu1iJBxcs8HF2ksHIYo0gIdEwgQ8cOsXLx8jNkfk8f4GMzO1yeLJA1gAcN2g1KrZAfKqWOlqOM99z5welS7TJywj78hLqz2MZWvK9mWnO8HGzgjw3X07IFOgr0mET2B2JcacT1DsVnf8pyEyhB2bPhMBzO5teBD72QV4iICk7RPtSVsyyxEz4mW/WQyyirntjsllhnyLQk+0QMsebh2A0C6O+W+Pe92y3S/VxNz2kGR5ToQPQgBavxkuSDUqmTkXX5LyL2sEbYAAmCYedzFIgpuIjswlIk402tMVkiRawcr8y3RKqsirpftSG7J332W2azVNig1XFwcK//teH7OKIlkfW2UDT/S7ldjDwQPTiZmy7jFLg8rkKy/n+fL+HQSnoYgqkQUN3Xem4SFyW/BV4S8010frWB1/YVFZblfNfQ8RvxljCYi2OZTACEUqXQf1aROvcwq3nV1I4e1dKdxKjPCmvFXv51fUol5w+70u6s6HvgpwVyDl78tJSGkHRHj0MmJNwcPUcRe2G2OtXKSfq/y5JJi/E9TyfD/sMn7NhvX0QkOuNiv2Y+WS11jXFF+lMGZgJFpIEf27c6sFJ90OqXbyagre7Fxfcw2WIYrvnH8wP4gmQFT81=="
        # 输入用户名和ua，验证是否出现滑动验证码
        self.if_appear_slice_url = "https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8"

        # 验证用户名明码，返回交换st码的url
        self.login_url = "https://login.taobao.com/member/login.jhtml"

        # 使用st发起请求，获取登陆cookie
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'

        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://login.taobao.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://login.taobao.com/member/login.jhtml',
        }

    def start_requests(self):
        """将用户名和ua发送到服务器"""
        if_appear_slice_formdata = {
            "username": "13066882860",
            "ua": self.ua
        }
        yield FormRequest(self.if_appear_slice_url,
                          formdata=if_appear_slice_formdata,
                          headers=self.headers,
                          callback=self.if_appear_slice
                          )

    def if_appear_slice(self, response):
        """验证是否出现滑动验证码"""
        verify_password_formdata = {
            "TPL_username": self.user_name,
            "ncoToken": "3828007e7eefddabf8ffb377504e5207d9e7cd0c",
            "slideCodeShow": "false",
            "useMobile": "false",
            "lang": "zh_CN",
            "loginsite": "0",
            "newlogin": "0",
            "TPL_redirect_url": "https://www.taobao.com/",
            "from": "tb",
            "fc": "default",
            "style": "default",
            "keyLogin": "false",
            "qrLogin": "true",
            "newMini": "false",
            "newMini2": "false",
            "loginType": "3",
            "gvfdcname": "10",
            "gvfdcre": "68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D613231626F2E323031372E3735343839343433372E372E35616639313164397030584C656326663D746F70266F75743D7472756526726564697265637455524C3D68747470732533412532462532467777772E74616F62616F2E636F6D253246",
            "TPL_password_2": "13eb0b6f1578eac715ed250a03230669c8edcd695e1b80ab56cdea2b7435b623ba34e1f478f2d837cce5ccca36d14a21d7c191d7c0ee08eb9a925cb8de4d109165a44f3cbb07acce93063c1b5ebad07b8f573905764dc34ae62b1f0d830b5c81b6f2ade4b15bb5deaac873d4e18ea6eba4fca724bc74361615d94b0cd9585e94",
            "loginASR": "1",
            "loginASRSuc": "1",
            "oslanguage": "zh-CN",
            "sr": "1366*768",
            "osVer": "windows|6.1",
            "naviVer": "chrome|63.03239132",
            "osACN": "Mozilla",
            "osAV": "5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "osPF": "Win32",
            "appkey": "00000000",
            "mobileLoginLink": "https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/&useMobile=true",
            "um_token": "T6352E6DEEB961D2F2BFA5DB0149731AFED2FC5203E361593CDD469E122",
            "ua": self.ua,
        }
        resp = response.text
        resp = json.loads(resp)
        needcode = resp.get("needcode")
        if needcode:
            print("需要滑动滑块")
        else:
            yield FormRequest(url=self.login_url,
                              headers=self.headers,
                              formdata=verify_password_formdata,
                              callback=self.get_url_for_st,
                              )

    def get_url_for_st(self, response):
        # print(response.text)
        get_st_url = re.search(r'<script src="(.*?)"></script>', response.text)
        if not get_st_url:
            print("获取st码url失败")
        else:
            yield Request(url=get_st_url.group(1), headers=self.headers, callback=self.get_st_code)

    def get_st_code(self, response):
        """携带st码发送一个请求到服务器即可获取cookie"""
        st_code = re.search(r'"data":\{"st":"(.*?)"\}\}', response.text)
        if not st_code:
            print("st码获取失败")
        else:
            st_url = self.vst_url.format(st_code.group(1))
            yield Request(url=st_url, headers=self.headers, callback=self.verify_login_result)

    def verify_login_result(self, response):
        """验证登陆是否成功，成功则开始爬取商品详情"""
        my_taobao_match = re.search(r'top.location.href = "(.*?)"', response.text)
        if my_taobao_match:
            print("淘宝登陆成功")
            search_url = 'https://s.taobao.com/search?q=%E7%B3%96%E5%B0%BF%E7%97%85%E9%9B%B6%E9%A3%9F&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=0&ntoffset=7&p4ppushleft=%2C44&sort=sale-desc&s={}'
            for i in range(0, 99):
                s = i * 44
                print(f"正在爬取第{i}页...")
                yield Request(url=search_url.format(s), headers=self.headers, callback=self.parse_page)
        else:
            print("淘宝登陆失败")

    def parse_page(self, response):
        resp = response.text
        goods_json = re.search(r"g_page_config = (.+?\}\});", resp)
        if goods_json:
            goods_dict = json.loads(goods_json.group(1))
            goods_list = goods_dict["mods"]["itemlist"]["data"]["auctions"]
            for goods in goods_list:
                title = goods["title"]
                raw_title = goods["raw_title"]
                view_price = goods["view_price"]
                detail_url = goods["detail_url"]
                item_loc = goods["item_loc"]
                view_sales = goods["view_sales"]
                comment_count = goods["comment_count"]

                items = TaobaoItem(title=title, raw_title=raw_title, view_price=view_price,
                                   detail_url=detail_url, item_loc=item_loc, view_sales=view_sales,
                                   comment_count=comment_count)
                # print(dict(items))
                yield items
        else:
            print("没有找到")
