import soundfile as sf
import madmom
import librosa
import os
import numpy as np
import json

def readAudio(inputFilePath):
    x, fs = sf.read(inputFilePath)
    if x.shape[1] == 2:
        x = x[:, 1]
    return x, fs

def writeAudio(outputFilePath, x, fs):
    sf.write(outputFilePath, x, fs)


pitch_classes = {
    'C' : 0, 
    'C#' : 1, 
    'D' : 2, 
    'D#' : 3,
    'E' : 4,
    'F' : 5,
    'F#' : 6,
    'G' : 7,
    'G#' : 8,
    'A' : 9,
    'A#' : 10,
    'B' : 11,
}

def extractTempo(filePath):
    y, sr = readAudio(filePath)
    return librosa.beat.tempo(y = y, sr = sr)[0] # returning the first element of the tempo array

def extractPitchClass(filePath):
        key_probabilities = madmom.features.key.CNNKeyRecognitionProcessor()
        key_prediction = madmom.features.key.key_prediction_to_label(key_probabilities(filePath))
        key, mode = key_prediction.split()
        pitchClass = pitch_classes[key]
        if (mode == 'major'):
            pitchClass = (pitchClass - 3) % 12
    
        return pitchClass

def createFeatureDict(inputFolderPath):
    
    """
    Returns a dictionary with names of songs as keys and the tempo and key as the values
    """

    tempoDict = {}
    pitchClassDict = {}
    featureDict = {}
    for file in os.listdir(inputFolderPath):
        songName = file.split('.')[-2]
        tempoDict[songName] = extractTempo(os.path.join(inputFolderPath, file))
        pitchClassDict[songName] = extractPitchClass(os.path.join(inputFolderPath, file))
    featureDict["tempo"] = tempoDict
    featureDict["pitchClass"] = pitchClassDict
    featureDict["avgTempo"] = np.mean(list(tempoDict.values()))        
    featureDict["avgPitchClass"] = np.mean(list(pitchClassDict.values()))
    
    # Export as json file
    with open("featureDict.json", 'w') as f:
        json.dump(featureDict, f)
    
    return featureDict



