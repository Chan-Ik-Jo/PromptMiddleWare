import requests
import json
import openai
class prototype:
    
    def __init__(self,text):
        self.text = text
        self.Trash_Link = ["tistory", "kin", "youtube", "blog", "book", "news", "dcinside", "fmkorea", "ruliweb", "theqoo", "clien", "mlbpark", "instiz", "todayhumor"]
        with open('./secrets.json') as f:
            secrets = json.loads(f.read())
        self.Google_API_KEY = secrets['Google_API_KEY']
        self.Google_SEARCH_ENGINE_ID = secrets['Google_SEARCH_ENGINE_ID']
        self.Openai_API_KEY = secrets['OPENAI_API_KEY']
        self.start_page = 10
        
    # keyword extraction from input prompt 
    def extraction(self,text):
        keyword = text
        return text
    
    #extracted keyword send to search engine
    def get_search_api(self,text):
        url = f"https://www.googleapis.com/customsearch/v1?key={self.Google_API_KEY}&cx={self.Google_SEARCH_ENGINE_ID}&q={text}&start={self.start_page}"
        response = requests.get(url).json()
        return response #return type JSON
    
    # process search results
    def text_processing(self,text):
        ex_text = self.extraction(text)
        response = self.get_search_api(ex_text)
        data = response.get("items")
        return data#return JSON type for text delivery to LLM
    
    # processed search results send to LLM for Summarization
    def get_LLM(self,data,prompt_input,sys):
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                            messages=[{'role':'user','content': prompt_input},
                                                       {'role':'system', 'content': sys},
                                                       {'role' : 'assistant', 'content': data}]
                                            )
        return response
    #final output
    def out_put(self,response):
        print(response)
        


if __name__ == "__main__":
    text = input("input prompt : ")
    middle = prototype(text)
    print(middle.extraction(text))