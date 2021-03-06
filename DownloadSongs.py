import os
import json
import numpy as np
from tqdm import tqdm
import requests
from pydub import AudioSegment
# import youtube_dl
#spotdl documentation: https://pypi.org/project/spotdl/

DOWNLOAD_FOLDER = "./songs/fullSongs/"
PREVIEW_FOLDER = "./songs/previewSongs/"
PREVIEW_WAV_FOLDER = "./songs/previewWavs/"
JSON_PATH = './data/songlist_test.json'

# Download songs from youtube: 
def downloadYoutube(link):
    video = youtube_dl.YoutubeDL({}).extract_info(link, download=False)
    songName = f"{video['title']}.wav"
    if not os.path.exists(DOWNLOAD_FOLDER + songName):
        os.system(f"youtube-dl --extract-audio --audio-format wav -o \"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s\" {link}")
    return songName

# Download songs from spotify
def downloadSpotify(link, songPath):
    if not os.path.exists(songPath):
        print(link, songPath)
        os.system(f"spotdl {link} --path-template \'{songPath}\' --output-format wav")

def downloadPreview(url, songName):
    fileName = songName + ".mp3"
    filePath = os.path.join(PREVIEW_FOLDER,fileName)
    # note the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filePath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)

def transferToWav(src,dst):
        sound = AudioSegment.from_mp3(src)
        sound.export(dst,format="wav")

class ParseSongList:
    def __init__(self, jsonFilePath):
        self._jsonFilePath = jsonFilePath
        
        with open(jsonFilePath, "r") as f:
            file = (json.load(f))
            self._songList = json.loads(file)
            

    def getSongLinks(self):
        links = []
        for song in self._songList:
            links.append(song['external_urls']) 
        return links

    def getPreviews(self):
        urls = []
        for song in self._songList:
            urls.append(song['preview_url']) 
        return urls


    def getSongName(self, link):
        for song in self._songList:
            if song['external_urls'] == link:
                songName = song['songName']
                return songName

    # get song link by name            
    def getSongLink(self, name):
        for song in self._songList:
            if song['songName'] == name:
                songLink = song['external_urls']
                return songLink

    def getPreviewLink(self,link):
        for song in self._songList:
            if song['external_urls'] == link:
                songPreview = song['preview_url']
                return songPreview
                
    def getSongId(self, link):
        for song in self._songList:
            if song['external_urls'] == link:
                songId = song['songId']
                return songId

    def getTempo(self, songName):
        # read tempo from json file
        for song in self._songList:
            if song['songName'] == songName:
                tempo = song['songTempo']
                return tempo

    def getKeyandMode(self, songName):
        # read key and mode from json file
        for song in self._songList:
            if song['songName'] == songName:
                key = song['songKey'] # integers from 0 to 11
                mode = song['songMode'] # 1: Major, 0: minor
                return key, mode

    def setBoundaries(self,songName, bounds):
        for i, song in enumerate(self._songList):
            if song['songName'] == songName:
                with open(self._jsonFilePath, 'r+') as f:
                    data = json.loads(json.load(f))
                    data[i].update({'boundaries' : bounds})
                    f.seek(0)
                    f.write(json.dumps(json.dumps(data)))

    def getBoundaries(self, songName):
        for song in self._songList:
            if song['songName'] == songName:
                boundaries = song['boundaries']
                return boundaries
    

    def getPreview(self,songName):
        for song in self._songList:
            if song['songName'] == songName:
                preview = song['preview_url']
                if(preview == None):
                    print("No preview Link")

    
     
                
if __name__ == "__main__":
    
    # songList = ParseSongList(JSON_PATH)
    # links = songList.getSongLinks()

    # print(songList,links)

    # for link in tqdm(links[11:12]):
    #     songName = songList.getSongName(link)
    #     songPath = DOWNLOAD_FOLDER + songName + '.wav'
    #     print(songName)
        

    #     # if not os.path.exists(songName):
    #     downloadSpotify(link, songPath)

    songList = ParseSongList(JSON_PATH)
    links = songList.getSongLinks()
    urls = songList.getPreviews()
    print(songList, urls)
    for link in tqdm(links[0:20]):
        songName=songList.getSongName(link)
        songPreview =songList.getPreviewLink(link)
        if(songPreview!=None):
            downloadPreview(songPreview,songName)
            src = PREVIEW_FOLDER+songName+".mp3"
            dst = PREVIEW_WAV_FOLDER+songName+".wav"
            print(src,dst)
            transferToWav(src,dst)
        else:
            print(f"No preview Link for {songName}")