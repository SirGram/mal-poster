from bs4 import BeautifulSoup
import requests
import os
import random
import glob
import threading
from PIL import Image


thread_list = []
searchlist = []
image_url_list=[]

total_searches = 0
validated_files=0

def init():

    #Create dir
    global dir
    dir="static/ANIMEIMAGES"
    if not os.path.exists(dir):
        os.mkdir(dir)

    # Read list_of_anime.txt
    with open("static/list_of_animes.txt", errors="ignore") as f:
        lines = f.readlines()
        for line in lines:
            searchlist.append(line.strip())
    global MAX_SEARCHES
    MAX_SEARCHES = len(searchlist)
    print(f"Searching for: {MAX_SEARCHES}")
def soup_mal():
    try:


        search = searchlist[random.randrange(len(searchlist))]
        searchlist.remove(search)

        # Get search url
        req = requests.get(f"https://myanimelist.net/search/all?q={search.lower()}&cat=all")
        soup = BeautifulSoup(req.text, "html.parser")
        data = soup.find_all("div", {"class": "title"})
        a_class = data[0].find_all('a')
        anime_url = a_class[0].get('href')

        # Get anime images
        req2 = requests.get(f"{anime_url}/pics")
        soup2 = BeautifulSoup(req2.text, "html.parser")
        data2 = soup2.find_all("div", {"class": "picSurround"})
        for item in data2:
            a_class = item.find_all("a")
            image_url = a_class[0].get('href')
            image_url_list.append(image_url)

        #Download images
        download_images(search)

    except:
        print("error")
        return
def download_images(search):
    try:
        global total_searches
        # Download images
        random.shuffle(image_url_list)
        img_data = requests.get(image_url_list[0]).content
        with open(f"{dir}/{search}{random.randrange(1000)}.png", "wb") as f:
            f.write(img_data)
            print(f"Downloaded {total_searches} images")

        total_searches+=1
    except:
        return
def valid_files():

    lst=os.listdir("./static//ANIMEIMAGES")
    validated_files=len(lst)
    print(f"Downloaded valid files: {validated_files}")
    return validated_files

def clean_files():
    files = glob.glob("./static/ANIMEIMAGES/*")
    for f in files:
        if os.path.getsize(f) < 10:
            # Delete invalid files
            os.remove(f)
        else:
            # Delete horizontal images
            im = Image.open(f)
            im_relation = im.width / im.height
            im.close()

            if im_relation<0.60 or im_relation>0.75:
                os.remove(f)
def worker():
    soup_mal()


def main():
    for i in range(MAX_SEARCHES):
        t = threading.Thread(target=worker)
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()

    valid_files()
    clean_files()

if __name__=="__main__":
    init()
    main()



