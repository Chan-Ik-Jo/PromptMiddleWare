#%%
import requests
import json
import openai
import numpy as np
from numpy.linalg import norm
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
from test import Google_API
import certifi

import urllib3
import time

#%%
http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
        )
'''
현재 문제

1. 키워드 추출
2. 같은 곳으로 트래픽 많이보내면 아이피 벤 관련(어쩔 수 없음 사이트 정책에 걸려서)
3. openai 토큰 길이 제한(단 gpt 3.5 turbo일 경우)

'''
class prototype:
    
    def __init__(self):
        self.Trash_Link = ["tistory", "kin", "youtube", "blog", "book", "news", "dcinside", "fmkorea", "ruliweb", "theqoo", "clien", "mlbpark", "instiz", "todayhumor"]
        with open('./secrets.json') as f:
            secrets = json.loads(f.read())
        self.Google_API_KEY = secrets['Google_API_KEY']
        self.Google_SEARCH_ENGINE_ID = secrets['Google_SEARCH_ENGINE_ID']
        openai.api_key = secrets['OPENAI_API_KEY']
        self.search_number = 20

        
    # keyword extraction from input prompt 
    def extraction(self,text):
        
        '''
        프롬프트에 대한 키워드 추출 지금 모델을 설계 하는게 맞는 판단인지 고민 중...
        
        '''
        
        keyword = text
        return text
    
    #extracted keyword send to search engine
    def get_search_api(self,text):  
        return Google_API(text,self.search_number)
    
    # processed and data filtering to search results
    def text_processing(self,text):
        ex_text = self.extraction(text)
        #response data type : dataframe
        response = self.get_search_api(ex_text)
        preview_data = []
        # response = pd.read_csv('./search_frame.csv')
        #emb_list type : dict
        prompt_emb = self.get_prompt_embedding(text)
        emb_list = self.get_search_embedding(response)
        cos_topid_list = self.get_cos(prompt_emb,emb_list)
        # print(len(cos_topid_list))
        for i in range(len(cos_topid_list)):
            preview_data.append(emb_list[cos_topid_list[i]])
        return preview_data #cosine similarity top 10 data
    
    
    def get_data(self,preview_data):
        content =[]
        for i in range(len(preview_data)):
            text = self.get_page_content(preview_data[i]['link'])
            content.append(text)
        return text

    # processed search results send to LLM for Summarization
    def get_LLM(self,data,prompt_input):
        response = openai.ChatCompletion.create(model='gpt-4-turbo',
                                            messages=[{'role':'user','content': prompt_input},
                                                       {'role':'system', 'content': "주어진 정보로 바탕으로 얘기해줘"},
                                                       {'role' : 'assistant', 'content': data}]
                                            )
        return response
    def get_prompt_embedding(self,text):
        emb_response = openai.Embedding.create(model = 'text-embedding-ada-002',input=text)
        return emb_response['data'][0]['embedding']
    
    def get_page_content(self,preview_data):
        test=[]
        for i in range(len(preview_data)):
            link = preview_data[i]['link']
            try:
                http = urllib3.PoolManager(
                    cert_reqs='CERT_REQUIRED',
                    ca_certs=certifi.where()
                )
                response = http.request('GET', link)
                if response.status == 200:
                    html = response.data.decode('utf-8')
                    soup = bs(html, 'html.parser')
                    text = soup.get_text()
                    text = text.replace('\n', '').replace('\r', '')
                    print(text)
                    test.append(text)
                else:
                    print("Error:", response.status)
            except Exception as e:
                print("Error:", e)
                
    
    def get_cos(self,prom,search):
        prom_emb = np.array(prom)
        search_emb = []
        result =[]
        topid =[]
        for i in range(len(search)):
            search_emb.append(np.array(search[i]['embedding']))
        # print(search_emb)   
        for i in range(len(search)):
            cos = np.dot(search_emb[i],prom_emb)/(norm(search_emb[i])*norm(prom_emb))
            result.append(cos)
        print(result)
        sorted_li= sorted(result)[-10:]
        for i in range(len(sorted_li)):
            topid.append(result.index(sorted_li[i]))
        return topid # type list
    
    def get_search_embedding(self,response):
        link_list = response['Link'].values.tolist()
        des_list = response['Description'].values.tolist()
        print(type(des_list))
        print(des_list)
        data = []
        for i in range(0,len(des_list)): #length 20
            emb = {}
            text = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·&・;○～]', ' ', des_list[i])
            text = ' '.join(text.split())
            # print(value)
            emb_response = openai.Embedding.create(model = 'text-embedding-ada-002',input=text)
            emb['link'] = link_list[i]
            emb['txt'] = text
            emb['embedding']= emb_response['data'][0]['embedding']
            # print(emb)
            data.append(emb)
            # print(data[i]['txt'])
        # print(data)
        json.dump(data,open('embedding.json','w'))
        return data
            
    #final output
    def out_put(self,response):
        print(response)
#%%     
if __name__ == "__main__":
    text = input("input prompt : ")
    middle = prototype()
    preview_data=middle.text_processing(text) #keyword 추출, 검색결과, 결과 embedding,query embedding,cosine similarity
    data = middle.get_page_content(preview_data) #여러개의 링크에 request 보내는 부분
    print(data)#링크 본문 텍스트
    result = middle.get_LLM(','.join(data),text) # send LLM(gpt-3.5-turbo)
    result = middle.out_put(result['choices'][0]['message']['content']) #final output