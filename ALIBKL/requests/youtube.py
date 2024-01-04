import requests

def playlist_name(link):
    reqs = requests.get(link, cookies={'CONSENT': 'YES+'}).text
    spli = reqs.split('"')
    for i in range(len(spli) - 2):
        if spli[i + 2] == "numVideosText":
            return spli[i]



def get_all_video_links(link):
    if ".caca" in link:
        f = open(link)
        text = f.read()
        f.close()
    else:
        reqs = requests.get(link, cookies={'CONSENT': 'YES+'})
        text = reqs.text
        reqs.close()
    urls = []
    spli = text.split('"')
    for i in spli:
        if "/watch?v=" in i:
            urls.append("youtube.com/" + i)
            print("youtube.com/" + i)
    urls = list(set(urls))
    return urls

def download_youtube_playlist_image(link, destination):
    reqs = requests.get(link, cookies={'CONSENT': 'YES+'})
    spli = reqs.text.split('"')
    url = ""
    for i in range(len(spli) - 2):
        if "i9.ytimg" in spli[i] and "maxresdefault" in spli[i]:
            url = spli[i].replace("\\u0026","\u0026")
            break
    if url == "":
        for i in range(len(spli) - 2):
            if "i.ytimg" in spli[i] and "hqdefault" in spli[i]:
                url = spli[i].replace("\\u0026", "\u0026")
                break
    img_data = requests.get(url)
    with open(destination + '/cover.jpg', 'wb') as handler:
        handler.write(img_data.content)
    from PIL import Image
    image = Image.open(destination + '/cover.jpg')
    sunset_resized = image.resize((1000, 1000))
    sunset_resized.save(destination + '/cover.jpg')