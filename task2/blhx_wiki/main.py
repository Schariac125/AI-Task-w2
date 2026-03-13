import requests
import json
import os
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    'Accept-Encoding': 'gzip'
}
def main():
    url="https://wiki.biligame.com/blhx/api.php"
    params={
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "list":"categorymembers",
        "maxlag": "5",
        "cmtitle": "Category:方案舰娘",
        "cmlimit": "500"
    }
    res=requests.get(url,params=params,headers=headers)
    filename="ship.json"
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(res.json(),f,ensure_ascii=False,indent=4)
    
    data=res.json()
    for item in data["query"]["categorymembers"]:
        url=f"https://wiki.biligame.com/blhx/{item['title']}"
        results=requests.get(url,headers=headers)
        path=os.path.join("output",f"{item['title']}.html")
        with open(path,"w",encoding="utf-8") as f:
            f.write(results.text)
if __name__ == "__main__":
    main()
    print("爬取完成了喵指挥官！")
