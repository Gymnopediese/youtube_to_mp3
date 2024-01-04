from pytube import YouTube
import requests
from moviepy.editor import *
import eyed3
from eyed3.id3.frames import ImageFrame
from pydub import AudioSegment
from glob import glob
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from threading import Thread
import music_tag

def get_all_video_links(link):
    reqs = requests.get(link, cookies={'CONSENT': 'YES+'})
    urls = []
    spli = reqs.text.split('"')
    for i in spli:
        if "/watch?" in i and len(i.split("=")) == 4:
            urls.append("youtube.com/" + i)
    return urls

def clean_title(title):
    title = title.split(" - ")[-1]
    title = remove_from_to(title, "(", ")")
    if title[-1] == " ":
        title = title[:len(title) - 1]
    title = title.replace("/", "-")
    return title

def youtube_to_mp3(link, destination = ".", tracknum = 0, cover = ""):
    global end
    tracknum = zeros(tracknum)
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    try:
        out_file = video.download(output_path=destination)
    except:
        end += 1
        return
    clean = clean_title(yt.title)
    if tracknum in clean:
        new_file = destination + "/" + clean_title(yt.title) + ".mp3"
    else:
        new_file = destination + "/" + tracknum  + "." + clean_title(yt.title) + ".mp3"
    AudioSegment.from_file(out_file).export(new_file, format="mp3")
    try:
        os.remove(out_file)
    except:
        pass
    audiofile = eyed3.load(new_file)
    audiofile.tag.track_num = tracknum
    if cover != "":
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(cover, 'rb').read(), 'image/jpeg')
    audiofile.tag.save()
    mp3 = MP3File(new_file)
    mp3.artist = destination
    mp3.album = destination
    mp3.track = tracknum
    mp3.set_version(VERSION_BOTH)
    mp3.save()
    print(yt.title + " has been successfully downloaded.")
    end += 1


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

def youtube_playlist_to_mp3(link, destination = "."):
    global end
    end = 0
    os.makedirs(destination ,exist_ok=True)
    download_youtube_playlist_image(link, destination)
    urls = get_all_video_links(link)
    for i in range(len(urls)):
        x = Thread(target=youtube_to_mp3, args=(urls[i], destination, i + 1, destination + "/cover.jpg"))
        x.start()
    while end < len(urls):
        pass

def main():
    while True:
        playlist = input("link please: ")
        if "playlist" in playlist:
            youtube_playlist_to_mp3(playlist, playlist_name(playlist))
        else:
            destination = input("destination please: ")
            youtube_to_mp3(playlist, destination)


def print_album_tags(dest):
    files = glob(dest + "/*")
    for i in files:
        if ".mp3" in i:
            print(i)
            mp3 = MP3File(i)
            print(mp3.get_tags())
            mp3.save()

def playlist_name(link):
    reqs = requests.get(link, cookies={'CONSENT': 'YES+'}).text
    spli = reqs.split('"')
    for i in range(len(spli) - 2):
        if spli[i + 2] == "numVideosText":
            return spli[i]

# Test the function

if __name__ == "__main__":
    main()
"""
https://i9.ytimg.com/s_p/OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU/mqdefault.jpg?sqp=CNCw2JgGir7X7AMGCLbRxJgG\u0026rs=AOn4CLCIxz5qEXP6HOyqyOeAFvDNDIdqGg\u0026v=1662068918

https://i9.ytimg.com/s_p/OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU/mqdefault    .jpg?sqp=CMjt2JgGir7X7AMGCLbRxJgG&amp;rs=AOn4CLCdc_3ovFg9dfXnyd8mhLCx_Gcc1Q&amp;v=1662068918&amp;days_since_epoch=19240

https://i9.ytimg.com/s_p/OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU/maxresdefault.jpg?sqp=CJzr2JgGir7X7AMGCLbRxJgG&rs=AOn4CLBqRwNQP7pgzV5yT-VhZIIlDM37fQ&v=1662068918
                         OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU


https://i9.ytimg.com/s_p/OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU/maxresdefault.jpg?sqp=CMjt2JgGir7X7AMGCLbRxJgGrs=AOn4CLCld9bQOW7Ny2932gfdNZSVxaFTugv=1662068918
"""