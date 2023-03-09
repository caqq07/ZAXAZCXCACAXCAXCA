import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style, init
import re


def clearifycontent(text: str):
    tnetx = text
    urls = re.findall("(?P<url>https?://[^\s]+)", tnetx)
    for i in urls:
        tnetx = tnetx.replace(i, "")
    
    return tnetx



def login_and_send(username: str, password: str, group_url: str, text: str, tag: str):
    session = requests.session()
    session.headers = {
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    session.post("https://coinfeedback.io/requests.php?f=login", data={
        "username": username,
        "password": password,
        "remember_device": "on"
    })

    r    = session.get(group_url)
    soup = BeautifulSoup(r.content, 'lxml')

    hash_id  = soup.find("input", attrs={"name":"hash_id"}).attrs['value']
    group_id = soup.find("input", attrs={"name":"group_id"}).attrs['value']
    

    r = session.post("https://coinfeedback.io/requests.php?f=posts&s=insert_new_post", data={
        "postText": clearifycontent(text),
        "album_name": "",
        "feeling": "",
        "feeling_type": "",
        "filename": "",
        "answer": "",
        "answer": "",
        "postMap": "",
        "post_color": "",
        "postPhotos": "",
        "postFile": "",
        "parts": "",
        "group_id": group_id,
        "hash_id": hash_id,
        "postRecord": "",
        "postSticker": ""
    })
    post_id = r.json()['post_id']
    print(Fore.LIGHTGREEN_EX  + f"[ {tag} ] {post_id} ID'li gönderi paylaşıldı: https://coinfeedback.io/post/{post_id}_baslik.html .")


# login_and_send("garrison.sanford_942", "123456", "https://coinfeedback.io/ethereum", "this is elon musk!")
