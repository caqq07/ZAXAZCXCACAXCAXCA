import time
import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder


class CoinFeedClient():
    def __init__(self) -> None:
        self.session = requests.session()
        self.session.headers = {
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }


    def save_image(self, url: str):
        r = requests.get(url)
        name = str(time.time())
        open("photos\\" + name + ".jpg", "wb").write(r.content)

        return "photos\\" + name + ".jpg"


    def login(self, username: str, password: str) -> None:
        r = requests.post("https://coinfeedback.io/api/auth", data={
            "server_key": "4628be790f74a503f1c8d56339ff8689",
            "username": username,
            "password": password,
            "device_type": "windows"
        })
        # print(r.content)

        self.access = r.json()['access_token']


    def send_post_with_photo(self, content: str, imageUrl: str) -> int:
        # imageUrl = ("file.jpg", open("sadsa.jpg", "rb"), "image/jpeg")
        r = requests.post("https://coinfeedback.io/api/new_post?access_token=" + self.access, data={
            "server_key": "4628be790f74a503f1c8d56339ff8689",
            "postText": content,
            "album_name" :"",
            "feeling": "",
            "feeling_type": "",
            "answer": "",
            "postMap": "",
            "post_color": "",
            "postFile": "",
            "group_id": "",
            "postSticker": "",
            "postRecord": "",
        }, files=[
            ('postPhotos[]',("file.jpg", open(self.save_image(imageUrl), "rb"), "image/jpeg"))
        ])

        print(r.content, r)

        try:

            post_id = r.json()['post_data']['post_id']
        except:
            return "0X000"

        return post_id

    
    def send_post_without_photo(self, content: str, f=0) -> int:
        # imageUrl = ("file.jpg", open("sadsa.jpg", "rb"), "image/jpeg")
        r = requests.post("https://coinfeedback.io/api/new_post?access_token=" + self.access, data={
            "server_key": "4628be790f74a503f1c8d56339ff8689",
            "postText": content,
            "album_name" :"",
            "feeling": "",
            "feeling_type": "",
            "answer": "",
            "postMap": "",
            "post_color": "",
            "postFile": "",
            "group_id": "",
            "postSticker": "",
            "postRecord": "",
        })

        

        try:

            post_id = r.json()['post_data']['post_id']
        except:
            if not f:
                return self.send_post_without_photo(content=content, f=1)
            return "0X000"

        return post_id

import re


def clearifycontent(text: str):
    tnetx = text
    urls = re.findall("(?P<url>https?://[^\s]+)", tnetx)
    for i in urls:
        tnetx = tnetx.replace(i, "")
    
    return tnetx

import json
def find_id(url: str):
    url = url.split("&u=")[-1].lower()
    for i in json.load(open("zozo.json", "r", encoding="utf-8"))['data']:
        if url == i['group_name']:
            return i['id']

def login_and_send(username, password, group_url, content: str, tag) -> int:
    r = requests.post("https://coinfeedback.io/api/auth", data={
            "server_key": "4628be790f74a503f1c8d56339ff8689",
            "username": username,
            "password": password,
            "device_type": "windows"
        })
    print(r.content)

    access = r.json()['access_token']

    group_id = find_id(group_url)
    # imageUrl = ("file.jpg", open("sadsa.jpg", "rb"), "image/jpeg")
    r = requests.post("https://coinfeedback.io/api/new_post?access_token=" + access, data={
            "server_key": "4628be790f74a503f1c8d56339ff8689",
            "postText": content,
            "album_name" :"",
            "feeling": "",
            "feeling_type": "",
            "answer": "",
            "postMap": "",
            "post_color": "",
            "postFile": "",
            "group_id": group_id,
            "postSticker": "",
            "postRecord": "",
    })

    try:

        post_id = r.json()['post_data']['post_id']
        print(post_id)
        return post_id
    except:
        #if not tag:
            # return login_and_send(content=content, f=1)
        return "0X000"

    return post_id
