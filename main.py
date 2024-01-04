import time

from pytube import YouTube
import requests
from moviepy.editor import *
from pydub import AudioSegment
from glob import glob
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from threading import Thread
import sys
from ALIBKL.kofl.progress_bar import printProgressBar

from ALIBKL.inputs.ask import ask_y_n_Y_N
from ALIBKL.inputs.ask import ask_options
from ALIBKL.audio.tags import change_mp3_tag
from ALIBKL.requests.youtube import *
from ALIBKL.int.zeros import zeros
from ALIBKL.audio.lyrics import get_lyrics
from get_title import clean_title

"""
def img():
    f = music_tag.load_file("nokia/test/Zed Yun Pavarotti - Iles (Clip Officiel).mp3")
    with open('unnamed-9.png', 'rb') as img_in:
        f['artwork'] = img_in.read()
    with open('unnamed-9.png', 'rb') as img_in:
        f.append_tag('artwork', img_in.read())
    f.save()
"""
end = 0
count = 0
from pytube import YouTube
def youtube_to_mp4(link, destination="."):
    try:
        video = YouTube(link)
    except:
        return
    # Get the highest resolution stream
    try:
        title = video.title.replace(".", "").replace(":", "").replace("/", "").replace("'", "")
    except Exception as e:
        title = ""
    if title == "" or not os.path.exists(destination + "/" + title + ".mp4"):
        print(destination + "/" + title + ".mp4")
        try:
            stream = video.streams.get_highest_resolution()
        except Exception as e:
            return
        # Download the video
        stream.download(destination)
        del stream
    del video
    return
def youtube_to_mp3(link, destination=".", tracknum=0, cover="default.jpeg"):
    global end
    tracknum = zeros(tracknum)
    yt = YouTube(link)
    clean = clean_title(yt.title)
    new_file = destination + "/" + clean + ".mp3"
    if os.path.exists(new_file):
        print(f"{new_file} already exist.")
        return
    try:
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=destination)
    except:
        return
    AudioSegment.from_file(out_file).export(new_file, format="mp3")
    try:
        os.remove(out_file)
    except:
        pass
    artist = yt.author.split(" - ")[0]
    print(f"new file {new_file}")
    change_mp3_tag(new_file, cover, artist, destination.split("/")[-1], tracknum, clean, get_lyrics(clean, artist))
    print(yt.title + " has been successfully downloaded.")
    end -= 1

def youtube_playlist_to_mp4(link, destination="."):
    end = 0
    count = 0
    t = 0
    urls = get_all_video_links(link)
    print(len(urls))
    os.makedirs(destination ,exist_ok=True)
    t = []
    for i in range(len(urls)):
        if end == 100:
            for thread in t:
                printProgressBar(count, len(urls), count, end)
                thread.join()
                count += 1
            t.clear()
            end = 0
        end += 1
        x = Thread(target=youtube_to_mp4, args=(urls[i], destination))
        x.start()
        t.append(x)
        printProgressBar(count, len(urls), count, end)
    for i in t:
        printProgressBar(count, len(urls), count, end)
        i.join()
        count += 1
    t.clear()





def youtube_playlist_to_mp3(link, destination="."):
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

def youtube_playlists_to_mp3(path):
    with open(path) as f:
        urls = f.read().split("\n")
    letgo = 0
    for i in urls:
        if "$" not in i:
            if not "playlist" in i:
                youtube_to_mp3(i, "sam")
            else:
                name = playlist_name(i)
                if name == None:
                    print(f"{i} is not a valid url.")
                    continue
                album = "sam/" + name
                if not os.path.isdir(album) or letgo == 1:
                        youtube_playlist_to_mp3(i, album)
                elif letgo != 2:
                    temp = ask_y_n_Y_N(f"{album} seem to already exist, would you like to download it again? y/n Y/N.")
                    if temp == 0:
                        youtube_playlist_to_mp3(i, album)
                    if temp == 2:
                        letgo = 1
                        youtube_playlist_to_mp3(i, album)
                    if temp == 3:
                        letgo = 2
                else:
                    print(f"{album} already exists.")



def read_inputs():
    mode = ask_options("questions/mode.txt", 0, 4)
    if mode == 0:
        print("Enter a Song link")
        link = input(">> ")
        destination = input("destination please: ")
        youtube_to_mp3(link, destination)
    elif mode == 1:
        print("Enter a Playlist link")
        playlist = input(">> ")
        youtube_playlist_to_mp3(playlist, playlist_name(playlist))
    elif mode == 2:
        print("Enter a <.tmp3> file")
        file = input(">> ")
        youtube_playlists_to_mp3(file)
    else:
        exit()

def main():
    # youtube_playlists_to_mp3("waitlist.tmp3")
    # return
    while True:
        read_inputs()



# Test the function

if __name__ == "__main__":
    # youtube_playlist_to_mp4(input("link\n>> "),
    #                         input("folder\n>> "))
    # exit(0)
    main()
"""
https://i9.ytimg.com/s_p/OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU/mqdefault.jpg?sqp=CNCw2JgGir7X7AMGCLbRxJgG\u0026rs=AOn4CLCIxz5qEXP6HOyqyOeAFvDNDIdqGg\u0026v=1662068918

https://i9.ytimg.com/s_p/OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU/mqdefault    .jpg?sqp=CMjt2JgGir7X7AMGCLbRxJgG&amp;rs=AOn4CLCdc_3ovFg9dfXnyd8mhLCx_Gcc1Q&amp;v=1662068918&amp;days_since_epoch=19240

https://i9.ytimg.com/s_p/OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU/maxresdefault.jpg?sqp=CJzr2JgGir7X7AMGCLbRxJgG&rs=AOn4CLBqRwNQP7pgzV5yT-VhZIIlDM37fQ&v=1662068918
                         OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU


https://i9.ytimg.com/s_p/OLAK5uy_lgPVqyOctPwBolSr-UIGErCgFKluspdKU/maxresdefault.jpg?sqp=CMjt2JgGir7X7AMGCLbRxJgGrs=AOn4CLCld9bQOW7Ny2932gfdNZSVxaFTugv=1662068918
"""