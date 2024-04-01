import urllib3
import requests
from bs4 import BeautifulSoup
import lxml
import re
header=  {
    'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'  
}
urllib3.disable_warnings()
def urllib3_request(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url,headers=header)
    urllib3.disable_warnings()
    soup = BeautifulSoup(response.data, "lxml").find_all('p')
    soup_text = ""
    for element in soup:
        soup_text += element.get_text() + "\n"
    return soup_text

def requests_request(url):
    li = []
    response = requests.get(url,headers=header,verify=False)
    
    soup=BeautifulSoup(response.text, 'html.parser').get_text()
    # soup_text = ""
    # for element in soup:
    #     soup_text += element.get_text()
    pattern = r'[^가-힣a-zA-Z0-9]'
    soup_text = re.sub(pattern, '', soup)
    return soup_text

# urllib = urllib3_request('https://www.kdi.re.kr/research/analysisView?art_no=3373')
# urllib = urllib3_request('https://www.melon.com')

request = requests_request('http://www.giikorea.co.kr/report/moi1404560-graphics-processing-unit-gpu-market-share-analysis.html')
# request = requests_request('https://www.melon.com')
# print(urllib)
print("=====================================")
print(request)