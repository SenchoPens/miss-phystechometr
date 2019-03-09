import os
from InstagramAPI import InstagramAPI

username = os.environ.get("INSTA_UNAME")
password = os.environ.get("INSTA_PSWD")

api = InstagramAPI(username, password)
api.login()

def get_igram_photos(uname, n=10):
    api.searchUsername(uname)
    userID = api.LastJson['user']['pk']

    api.getUserFeed(userID)
    info = api.LastJson

    return info['items'][0]['image_versions2']['candidates'][0]['url']
