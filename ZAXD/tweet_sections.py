import snscrape.modules.twitter as sntwitter
from websitemodules import login_and_send
import random
import time
from threading import Thread
from colorama import Fore, Back, Style, init
import os
import json


init(autoreset=True)


class userblacklist:
    blacklist = [i.replace("\n", "") for i in open("user_blacklist.txt", "r", encoding="utf-8").readlines()]
    max_hashtags = 0
    max_taggings = 0


config = json.load(open("config.json", "r", encoding="utf-8"))
userblacklist.max_hashtags = config['max_hashtags']
userblacklist.max_taggings = config['max_taggings']


def get_random_user():
    uuser, pwd = random.choice(open("users.txt", "r", encoding="utf-8").readlines()).replace("\n", "").split("\t")

    return uuser, pwd



def check_tag(tag: str, url: str):
    while True:
        try:
            counter = 0
            for tw in sntwitter.TwitterSearchScraper(tag).get_items():
                # tweet = vars(tw)
                tweet = tw
                # print(tweet)

                if counter == 10:
                    break
            
                counter += 1
                # print(tweet)
                if tweet.user.username not in userblacklist.blacklist and tweet.rawContent.count("#") < userblacklist.max_hashtags and tweet.rawContent.count("@") < userblacklist.max_taggings:
                    if str(tweet.id) not in open("system_files/" + "tweets_id.txt", "r", encoding="utf-8").read():
                        u, p = get_random_user()
                        try:
                            login_and_send(u, p, url, tweet.rawContent, tag)
                            open("system_files/tweets_id.txt", "a+", encoding="utf-8").write(str(tweet.id) + "\n")
                        except Exception as e:
                            print(e)
                            pass
                        
            
            print(Fore.LIGHTMAGENTA_EX + f"{tag} için bir döngü tamamlandı.")
            time.sleep(15)
        except Exception as e:
            print(e)
            time.sleep(10)
            check_tag(tag, url)
            pass
    


print(Fore.RED + f"Blacklist'te {len(userblacklist.blacklist)} kişi var.\n\n")
# print(Fore.RED + f"Blacklist'te {len(userblacklist.blacklist)} kişi var.")

for hashtag in open("hashtags.txt", "r", encoding="utf-8").readlines():
    time.sleep(1)
    tag, link = hashtag.replace("\n", "").split("||")
    print(Fore.GREEN + f"{tag} hashtag'i {link} adresinde paylaşılmak üzere çalışıyor.")

    app = Thread(target=check_tag, args=(tag, link))
    app.start()
