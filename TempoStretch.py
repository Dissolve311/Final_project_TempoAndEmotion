import soundfile as sf
import pyrubberband as pyrb
import utils
from DownloadSongs import ParseSongList
import os

SONG_PATH = "./songs/previewWavs/"
JSON_PATH = "./data/songlist_test.json"
# Read mono wav file
# y, sr = sf.read("./test.wav")
# print(y,sr)
# # Play back at double speed
# y_stretch = pyrb.time_stretch(y, sr, 2.0)
# print(y_stretch)
# outputFilePath = "./temp/test.wav"
# utils.writeAudio(outputFilePath,y_stretch,sr)


if __name__ == "__main__":
    ratio = float(input("The ratio you want:"))
    songLibrary = ParseSongList(JSON_PATH)
    print(songLibrary)
    # walk through fullSongs folder, get song name and then get song link
    for fileName in os.listdir(SONG_PATH):
        if not fileName.startswith('.') and os.path.isfile(os.path.join(SONG_PATH, fileName)):
            songName = fileName.split(" ")[0]
            songLink = songLibrary.getSongLink(songName)
            songPath = SONG_PATH + fileName
            print(songPath)
            y, sr = sf.read(songPath) 
            y_stretch = pyrb.time_stretch(y, sr, ratio)
            outputFilePath = f"./songs/temp/{fileName}"
            utils.writeAudio(outputFilePath,y_stretch,sr)
        