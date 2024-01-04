import eyed3
from eyed3.id3.frames import ImageFrame
from glob import glob

def change_mp3_tag(file, cover, artist, album, tracknum, name, lyrics):
    audiofile = eyed3.load(file)
    audiofile.tag.track_num = int(tracknum)
    if cover != "":
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(cover, 'rb').read(), 'image/jpeg')
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.title = name
    audiofile.tag.lyrics.set(str(lyrics))
    audiofile.tag.save()

def print_album_tags(dest):
    files = glob(dest + "/*")
    for i in files:
        if ".mp3" in i:
            print(i)
            mp3 = MP3File(i)
            print(mp3.get_tags())
            mp3.save()