import os
import pandas as pd
import numpy as np
import librosa
import joblib
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder


def extract_feature(y, sr):
    mfccs_features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    return mfccs_scaled_features



def predict_speaker(filename):

    model = tf.keras.models.load_model("./AudioProcessing/model_3.h5")

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

    features = [np.mean(chroma_stft), np.mean(rmse), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
    for e in mfcc:
        features.append(np.mean(e))
        
    features = np.array(features)
    features = features.reshape(1, features.shape[0])
    # header for dataframe
    df_columns = ["chroma_stft", "rmse", "spectral_centroid", "spectral_bandwidth", "rolloff", "zero_crossing_rate"]
    for i in range(13):
        df_columns.append(f"mfcc_{i}")

    df = pd.DataFrame(features)
    df.columns = df_columns
    
    # scale the features
    scaler = joblib.load("./AudioProcessing/preprocessing_helper/standard_scaler.joblib")
    X = scaler.transform(df)
    
    # predict
    y_p = model.predict(X)
    y_p = np.argmax(y_p, axis=1)
    
    # decode the labels
    label_encoder = joblib.load("./AudioProcessing/preprocessing_helper/label_encoder.joblib")
    return label_encoder.inverse_transform(y_p)