import os
from pydub import AudioSegment
from pydub.utils import make_chunks

SONG_PATH = "./songs/previewWavs/"
SEGMENT_PATH="./songs/segmentedSongs/"
def segmentAudio(file,length_ms):
    audio = AudioSegment.from_file(file , "wav")
    chunk_length_ms = length_ms
    chunks = make_chunks(audio, chunk_length_ms)
    fileName = file.split("/")[-1].split(".")[0]
    print(f"filename: {fileName}")
    #Export all of the individual chunks as wav files

    for i, chunk in enumerate(chunks):
        # only keep the first chunk
        if i!=0:
            break
        chunk_name = f"{SEGMENT_PATH}{fileName}_chunk{i}.wav"
        print ("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")

if __name__ == "__main__":
    for fileName in os.listdir(SONG_PATH):
        if not fileName.startswith('.') and os.path.isfile(os.path.join(SONG_PATH, fileName)):
            segmentAudio(SONG_PATH+fileName,20000)