def get_lyrics(song,artist):
    import lyricsgenius
    genius = lyricsgenius.Genius('e2A9WU7jf_azL7v8V3lVJzYu7fmKB43733d2R2PLADJ3Ke5cxmrFI1sCaiGagCre')
    try:
        return genius.search_song(song, artist).lyrics
    except Exception as e:
        print(e)
        return None