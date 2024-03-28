import requests
import pandas as pd
from bs4 import BeautifulSoup
import json 
import gensim
with open('./secrets.json') as f:
    secrets = json.loads(f.read())
Google_API_KEY = secrets['Google_API_KEY']
Google_SEARCH_ENGINE_ID = secrets['Google_SEARCH_ENGINE_ID']
Trash_Link = ["tistory", "kin", "youtube", "blog", "book", "news", "dcinside", "fmkorea", "ruliweb", "theqoo", "clien", "mlbpark", "instiz", "todayhumor"]
def Google_API(query, wanted_row):

    query= query.replace("|","OR")
    start_pages=[]

    df_google= pd.DataFrame(columns=['Title','Link','Description'])

    row_count =0


    for i in range(1,wanted_row+1000,10):
        start_pages.append(i)

    for start_page in start_pages:
        url = f"https://www.googleapis.com/customsearch/v1?key={Google_API_KEY}&cx={Google_SEARCH_ENGINE_ID}&q={query}&start={start_page}"
        data = requests.get(url).json()
        search_items = data.get("items")
        try:
            for i, search_item in enumerate(search_items, start=1): 
                link = search_item.get("link")
                if any(trash in link for trash in Trash_Link):
                    pass
                else: 
                    title = search_item.get("title")
                    descripiton = search_item.get("snippet")
                    df_google.loc[start_page + i] = [title,link,descripiton] 
                    row_count+=1
                    if (row_count >= wanted_row) or (row_count == 300) :
                        df_google.to_csv('test.csv')
                        return df_google
        except:
            return df_google

    
    return df_google