import urllib3
import requests
from bs4 import BeautifulSoup
import lxml
headers = {
    'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'  
}
def urllib3_request(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url,headers=headers)
    soup = BeautifulSoup(response.data, "lxml")
    soup_text = ""
    for element in soup:
        soup_text += element.get_text() + "\n"
    return soup_text

def requests_request(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser').find_all('p')
    soup_text = ""
    for element in soup:
        soup_text += element.get_text() + "\n"
    # text = soup.get_text()
    return soup_text

urllib = urllib3_request('https://ko.javascript.info/comparison')

request = requests_request('https://ko.javascript.info/comparison')

print(urllib)
print("=====================================")
print(request)