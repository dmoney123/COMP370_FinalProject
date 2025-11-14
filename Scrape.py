import requests
import json

url = "https://newsapi.org/v2/everything"
api_token = "02d9856ae6754ba899068431e06812c0"


#These will "edit" the request url after the ? sign in the base
params = {
    #many apis ignore unknown parameters, so not the end of the world if you add a parameter that is not supported

    "apiKey": api_token,
    "pageSize": 99,
    "q": "zohran mamdani",
    "sortBy": "popularity",
    "sources": "cnn,fox-news,msnbc",
}


#the meat and potatoes -> this requests the url:  https://api.thenewsapi.com/v1/news/all?api_token=ESyCcyvNPy337CFHT6RR3bQUzNOfht6W55Lfe8u4&country=us&language=en&category=politics&limit=5&keywords=Mamdami
response = requests.get(url, params=params)

# Print the actual URL that was called
print(f"Request URL: {response.url}")
#converts it to a json
test = response.json()


'''
#parsing through the request, needs the ["data"] part because thats where the articles are store in the json
for article in test["data"]:
    print(article["title"])
'''


#save a file
save_file = "articles.json"
import os

# Save to the same folder the script lives in
current_folder = os.path.dirname(os.path.abspath(__file__))
save_file = os.path.join(current_folder, "articles.json")

with open(save_file, "w") as f:
    #with pretty printing
    json.dump(test, f, indent=2, ensure_ascii=False)


