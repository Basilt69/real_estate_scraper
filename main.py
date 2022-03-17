import requests
from bs4 import BeautifulSoup
import json

class ZillowScraper():
    results = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'zguid=23|%249fd182d4-b853-4309-804f-ab3740135e02; zgsession=1|279753b1-fc6d-4203-baa9-02937d0b4c22; zjs_user_id=null; zg_anonymous_id=%224657c638-35a4-482b-a8f3-d4ca5a8c221b%22; zjs_anonymous_id=%229fd182d4-b853-4309-804f-ab3740135e02%22; _ga=GA1.2.716396384.1646904715; _pxvid=ed4f38c7-a054-11ec-8658-595373634672; _gcl_au=1.1.2012378296.1646904721; DoubleClickSession=true; __pdst=4f4f720de70446e5a403ff9d94df0ea1; _fbp=fb.1.1646904721467.2133605403; _pin_unauth=dWlkPU5UVmxaRFptTlRBdE5UYzBNeTAwTXprM0xXSmxPV0l0TUdZd1l6YzVaV0V6TkRsbA; QSI_SI_3G0KVrXaA2QHBlL_intercept=true; _cs_c=0; _cs_id=c662e181-a135-a18c-9420-389bc9160997.1647118325.1.1647118325.1647118325.1.1681282325645; JSESSIONID=7BAA25AEF56FCC23B586CC83078B53DD; _gid=GA1.2.1249983206.1647431881; KruxPixel=true; _clck=1c0yqg6|1|ezt|0; utag_main=v_id:017f732bbff5001c4e9ec1e7b73105073002306b00978$_sn:4$_se:1$_ss:1$_st:1647433683858$dc_visit:3$ses_id:1647431883858%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:1%3Bexp-session$dc_region:eu-central-1%3Bexp-session$ttd_uuid:8b3f4167-a91e-41f4-b1ed-5871ce1de1e5%3Bexp-session; KruxAddition=true; g_state={"i_p":1648036875173,"i_l":3}; search=6|1650024352437%7Cregion%3Dnew-york-ny%26rb%3DNew-York%252C-NY%26rect%3D40.917577%252C-73.700272%252C40.477399%252C-74.25909%26disp%3Dmap%26mdm%3Dauto%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%096181%09%09%09%09%09%09; _gat=1; _pxff_bsco=1; _px3=60eb08b67938e63623385da9592754cf2101eeadff10a0d91d01a8bccbb7db60:Onc+KfUt6bxJgYenco4/Ks4bOrqraHMQA2Ti7Y++wmG8hqcQ8x+zloMWVeFBEk4GH6I2Yd1gxO9LPqx6iBroGQ==:1000:V9cG/ZDd6qI6XmZmWpbNmH4rknrdZCGJ/N03KX+V5S3Ug6SavFGLsxLpWwWYhHSVtYYHRoFmJ8xkFFt8l882Jq1RSMEFNUUOueKkGdnPuM9IgoyyK8++OK6crbKrYCeP6Z6i9WwP1WEgV+J6TormkEaOfMOmuTwMER0NwovM+EqYm2M7FBfFkE7w2eS+eqO9og8orzqtnIuiBRk5RSRHog==; _uetsid=55e8d2c0a52011ec9d3d4fe7664d798b; _uetvid=f07b0a30a05411ecb0e565cee6d8e75d; AWSALB=TKxUI9BiEEZpdiLP4gAiaPTSkx99d02l9WA5SDLIcrEcX0zI5/d4m/0sxH9touImrCRFZrHASY99U8EkY/YPFzqiIOGq3fC41JnAj2+8LFnd8KFUDk8tyQwxalxT; AWSALBCORS=TKxUI9BiEEZpdiLP4gAiaPTSkx99d02l9WA5SDLIcrEcX0zI5/d4m/0sxH9touImrCRFZrHASY99U8EkY/YPFzqiIOGq3fC41JnAj2+8LFnd8KFUDk8tyQwxalxT; _clsk=18jybdj|1647432356211|4|0|f.clarity.ms/collect',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'
    }

    def fetch(self,url, params):
        response = requests.get(url, headers=self.headers, params=params)
        return response

    def parse(self,response):
        content = BeautifulSoup(response, 'lxml')
        #print(content.prettify())
        deck = content.find('ul', {'class':'photo-cards photo-cards_wow photo-cards_short '
                                          'photo-cards_extra-attribution'})
        for card in deck.contents:
            script = card.find('script', {'type':'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])

                #print(script.contents[0])
                try:
                    self.results.append({'name':script_json['name'],
                                     'floorSize':script_json['floorSize']['value']
                                     })
                except:
                    self.results.append({'name': script_json['name'],
                                         'floorSize': None
                                         })

        print(self.results)



    def run(self):
        url = 'https://www.zillow.com/new-york-ny/'
        params = {"pagination": {}, "usersSearchTerm": "New York, NY", "mapBounds": {"west": -74.46307943749999,
                                                                                     "east": -73.38367269921874,
                                                                                     "south": 40.44034254390936,
                                                                                     "north": 41.05065027021305},
                  "regionSelection": [{"regionId": 6181, "regionType": 6}], "isMapVisible": False,
                  "filterState": {"ah": {"value": True}, "sort": {"value": "globalrelevanceex"}}, "isListVisible": True}
        res = self.fetch(url,params)
        self.parse(res.text)

if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()



