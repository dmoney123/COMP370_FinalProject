import requests
import json
import os


def find_sources():
    url2 = "https://newsapi.org/v2/top-headlines/sources?apiKey=02d9856ae6754ba899068431e06812c0"
    response = requests.get(url2, params={"country": "us", "language": "en"})
    j = response.json()
    with open("source.json", "w", encoding="utf-8") as f:
        json.dump(j, f, ensure_ascii=False, indent=2)
    return
#find_sources()

    


url = "https://newsapi.org/v2/everything"
api_token = "02d9856ae6754ba899068431e06812c0"





params_list = []


#These will "edit" the request url after the ? sign in the base

"""
##FOX NEWS POST ELECTION##
params_1 = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "from": "2025-11-04",
    "to": "2025-11-13",
    "sources": "fox-news",
}


##CNN POST ELECTION##
params_2 = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "sources": "cnn",
    "from": "2025-11-04",
    "to": "2025-11-13",
}

##FOX NEWS PRE ELECTION##
params_3 = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "from": "2025-10-14",
    "to": "2025-11-04",
    "sources": "fox-news",
}

##CNN NEWS PRE ELECTION##
params_4 = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "from": "2025-10-14",
    "to": "2025-11-04",
    "sources": "reuters",

}

"""

#LEFT SOURCES PRE ELECTION##
Left_pre = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "from": "2025-10-14",
    "to": "2025-11-04",
    "sources": "msnbc,the-huffington-post,the-washington-post,newsweek,politico,vice-news,new-york-magazine",
}
#LEFT SOURCES POST ELECTION##
Left_post = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "from": "2025-11-04",
    "to": "2025-11-14",
    "sources": "msnbc,the-huffington-post,the-washington-post,newsweek,politico,vice-news,new-york-magazine",
}

#RIGHT WING SOURCES PRE##
Right_pre = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "from": "2025-10-15",
    "to": "2025-11-04",
    "sources": "breitbart-news,fox-news,national-review,the-american-conservative,the-washington-times",
}

#RIGHT WING SOURCES POST##
Right_post = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "from": "2025-11-04",
    "to": "2025-11-13",
    "sources": "breitbart-news,fox-news,national-review,the-american-conservative,the-washington-times",
}

#CENTER SOURCES PRE##
Center_pre = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "from": "2025-10-15",
    "to": "2025-11-04",
    "sources": "abc-news,associated-press,bloomberg,cbs-news,cnn,reuters,nbc-news,the-wall-street-journal,usa-today,the-hill,time,axios",
}
#CENTER SOURCES POST##
Center_post = {
    "apiKey": api_token,
    "pageSize": 100,
    "q": "zohran mamdani",
    "from": "2025-11-04",
    "to": "2025-11-13",
    "sources": "abc-news,associated-press,bloomberg,cbs-news,cnn,reuters,nbc-news,the-wall-street-journal,usa-today,the-hill,time,axios",
}


#params_list.append(("params_1", params_1))
#params_list.append(("params_2", params_2))
#params_list.append(("params_3", params_3))
params_list.append(("Right_post", Right_post))
params_list.append(("Center_post", Center_post))
params_list.append(("Left_pre", Left_pre))
params_list.append(("Left_post", Left_post))
params_list.append(("Right_pre", Right_pre))
params_list.append(("Center_pre", Center_pre))


#the meat and potatoes -> this requests the url:  https://api.thenewsapi.com/v1/news/all?api_token=ESyCcyvNPy337CFHT6RR3bQUzNOfht6W55Lfe8u4&country=us&language=en&category=politics&limit=5&keywords=Mamdami
# Save to the same folder the script lives in
current_folder = os.path.dirname(os.path.abspath(__file__))

for name, params in params_list:
    response = requests.get(url, params=params)
    print(f"Request URL: {response.url}")
    
    # Get the response data
    test = response.json()
    
    # Create filename using the variable name
    save_file = os.path.join(current_folder, f"{name}.json")
    
    # Save each request to a separate file
    with open(save_file, "w") as f:
        #with pretty printing
        json.dump(test, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to {save_file}")


'''
#parsing through the request, needs the ["data"] part because thats where the articles are store in the json
for article in test["data"]:
    print(article["title"])
'''



