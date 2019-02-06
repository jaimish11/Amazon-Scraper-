from lxml import html  
import csv,os,json
import requests
from time import sleep
import time
import numpy as np


 
def AmazonParser(url):
    t0 = time.time()
    user_agent = str(get_random_ua())
    headers = {'User-Agent': user_agent,}
    page = requests.get(url,headers=headers)
    while True:
        response_delay = time.time() - t0
        sleep(response_delay*5)
        try:
            #print(page)
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]/span[@id="productTitle"]/text()'
            XPATH_AVAIL = '//div[@id="availability"]/span[@class="a-size-medium a-color-price"]/text()'
            #XPATH_MANUFACTURER = '//div/a[@id="bylineInfo"]/text()'
            XPATH_PRICE = '//span[@id="priceblock_ourprice"]/text()'
            
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_AVAIL = doc.xpath(XPATH_AVAIL)
            #RAW_MANUFACTURER = doc.xpath(XPATH_MANUFACTURER)
            RAW_PRICE = doc.xpath(XPATH_PRICE)
            
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            AVAIL = ' '.join(''.join(RAW_AVAIL).split()) if RAW_AVAIL else 'Item available'
            PRICE = ' '.join(''.join(RAW_PRICE).split()).strip() if RAW_PRICE else None
            #MANUFACTURER = ' '.join(''.RAW_MANUFACTURER).strip() if RAW_MANUFACTURER else None
            print(NAME)
            print(AVAIL)
            print(PRICE)
            if page.status_code!=200:
                raise ValueError('captcha')
            data = {
                    'NAME': NAME,
                    'AVAILABILITY': AVAIL,
                    'PRICE': PRICE,
                    'URL':url,
                    }
 
            return data
        except Exception as e:
            print(e)
            
def ReadASIN():
    AsinList = [
    'B079H6RLKQ',
    'B07HR4FVDG',
    'B07K76LBLZ',
    'B06XRJQX91',
    'B076XLLCQC',
    'B079Z793SM',
    ]
    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.com/dp/"+i
        print("Processing: "+url)
        extracted_data.append(AmazonParser(url))
        sleep(5)
    f=open('data.json','a')
    json.dump(extracted_data,f,indent=4)
 
def get_random_ua():
    random_ua = ''
    ua_file = 'ua_file.txt'
    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_proxy = lines[int(idx)]
    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_proxy.strip()
    
if __name__ == "__main__":
    ReadASIN()