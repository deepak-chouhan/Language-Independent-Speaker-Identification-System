import os
# import pandas 
import numpy as np
# import matplotlib.pyplot as plt
import librosa
from sklearn import preprocessing
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import python_speech_features as mfcc

y = [2193057, 2193057, 2193057, 2193057, 2193057, 2193071, 2193071, 2193071, 2193071, 2193071, 2193119, 2193119, 2193119, 2193119, 2193119, 2193230, 2193230, 2193230, 2193230, 2193230, 2193263, 2193263, 2193263, 2193263, 2193263, 2193274, 2193274, 2193274, 2193274, 2193274, 2196003, 2196003, 2196003, 2196003, 2196003]

def extract_feature(y, sr):
    mfccs_features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    return mfccs_scaled_features



def predict_speaker(filename):
    
    # audio features
    audio, sr = librosa.load(filename, mono=True)
    audio, index = librosa.effects.trim(audio)
    
    # audio data
    mfcc = extract_feature(audio, sr)
    chroma_stft = librosa.feature.chroma_stft(y=audio, sr=sr)
    rmse = librosa.feature.rms(y=audio)
    spec_cent = librosa.feature.spectral_centroid(y=audio, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=audio, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(audio)

    feature = [np.mean(chroma_stft), np.mean(rmse), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
    for e in mfcc:
        feature.append(np.mean(e))
        
    feature = np.array(feature)
    # print(feature)
    feature = feature.reshape(1, feature.shape[0])

    # tranform X
    scaler = StandardScaler()
    X = scaler.transform(feature)
    
    # predict
    model1 = tf.keras.models.load_model("./AudioProcessing/model1.h5")
    y_p = model1.predict(X)
    y_p = np.argmax(y_p, axis=1)

    # label encoder
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    return label_encoder.inverse_transform(y_p)