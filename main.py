import requests
from bs4 import BeautifulSoup


class ZillowScraper:

    headers = {
        'accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, '
                  'image / apng, * / *;q = 0.8, application / signed - exchange; v = b3; q = 0.9',
        'accept - encoding': 'gzip, deflate, br',
        'accept-language': 'en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'zguid=23|%249fd182d4-b853-4309-804f-ab3740135e02; '
                  'zgsession=1|279753b1-fc6d-4203-baa9-02937d0b4c22; zjs_user_id=null; '
                  'zg_anonymous_id=%224657c638-35a4-482b-a8f3-d4ca5a8c221b%22; '
                  'zjs_anonymous_id=%229fd182d4-b853-4309-804f-ab3740135e02%22; _ga=GA1.2.716396384.1646904715; '
                  '_pxvid=ed4f38c7-a054-11ec-8658-595373634672; _gcl_au=1.1.2012378296.1646904721; KruxPixel=true; '
                  'DoubleClickSession=true; __pdst=4f4f720de70446e5a403ff9d94df0ea1; '
                  '_uetvid=f07b0a30a05411ecb0e565cee6d8e75d; _fbp=fb.1.1646904721467.2133605403; '
                  '_pin_unauth=dWlkPU5UVmxaRFptTlRBdE5UYzBNeTAwTXprM0xXSmxPV0l0TUdZd1l6YzVaV0V6TkRsbA; '
                  'utag_main=v_id:017f732bbff5001c4e9ec1e7b73105073002306b00978$_sn:1$_se:1$_ss:1$_st'
                  ':1646906521398$ses_id:1646904721398%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp'
                  '-session$tdsyncran:1%3Bexp-session$dc_visit:1$dc_event:1%3Bexp-session$dc_region:eu-central-1'
                  '%3Bexp-session$ttd_uuid:8b3f4167-a91e-41f4-b1ed-5871ce1de1e5%3Bexp-session; KruxAddition=true; '
                  '_px3=d00cbf2454874e576d6ae22ae73bcc83d6fa4f6e5462ce9781c4791c0829a297'
                  ':ZDcrREFlZyXIecIrT3yhLLmMRnb1w426gglczqYNA7kbcZfRE7grC1e+aRbqDPuLzwNcUW+cK/ZVQtb24RDALg==:1000'
                  ':xLpEf5gSZGhKpBWHyPXuCMAf83y3m151g/DpJecPI8UPRRSKe'
                  '+qqTErzTxbfrXXoYHR6ExISt6YGIP6oZupbbskgiQBiBjNlz3lS8VyK1UvpRC50p4yfQc2rz7vuWs53qJYwP23XbfAgvhDYnWBdNacJZ/iO1HZIyj1js+STybJSJGB97iABi2xrkJ/2BvIH431efQyiJYIhusaJYP3VPg==; _clck=1c0yqg6|1|ezo|0; _clsk=61infj|1647030702564|2|0|d.clarity.ms/collect; AWSALB=N5dsyBVRWQOcCSG+tJLUI/3uKwxP5eSBt7eo8IGjtPlcF2SxmaYbMsvF+raWPDMfuhosHQGqYaPrI6mkoCPjmCzAL+WI8qJGWyt8WmEaiPRULcLx00DmaO7IKlTk; AWSALBCORS=N5dsyBVRWQOcCSG+tJLUI/3uKwxP5eSBt7eo8IGjtPlcF2SxmaYbMsvF+raWPDMfuhosHQGqYaPrI6mkoCPjmCzAL+WI8qJGWyt8WmEaiPRULcLx00DmaO7IKlTk; JSESSIONID=32D79312068291D873CEBBD590FA940D; search=6|1649622702772%7Crect%3D41.30580088034345%252C-72.90027426171874%252C40.08430307138472%252C-75.05908773828124%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26lt%3Dfsba%252Cfore%252Cnew%252Ccmsn%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%096181%09%09%09%09%09%09',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }

    params = {
        'searchQueryState': '{"pagination": {}, "usersSearchTerm": "New York, NY", "mapBounds": {"west": '
                            '-75.05908773828124, "east": -72.90027426171874, "south": 40.08430307138472, '
                            '"north": 41.30580088034345}, "regionSelection": [{"regionId": 6181, "regionType": 6}], '
                            '"isMapVisible": false, "filterState": {"sort": {"value": "globalrelevanceex"}, '
                            '"ah": {"value": true}}, "isListVisible": true, "mapZoom": 9}'
    }
    def fetch(self, url, params):
        print('HTTP GET request to URL: %s', end='') % url
        res = requests.get(url, params=self.params, headers = self.headers)
        print(' | Status code: %s' % res.statues_code)

    def save_response(self, res):
        with open ('res.html', 'w') as html_file:
            html_file.write(res)

    def load_response(self):
        html = ''
        with open('res.html', 'r') as html_file:
            for line in html_file:
                html += line
        return html

    def parse(self, html):
        pass

    def to_csv(self):
        pass

    def run(self):
        res = self.fetch()

if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()