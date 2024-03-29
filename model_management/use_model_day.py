import numpy as np
import pandas as pd
from keras.models import load_model
import os

def predict_if_PumpDump(sciezka_do_pliku, data=None):
    best_model = load_model('Machine_learning/ML_model_and_data/model_epoch_307.hdf5')
    recent_data = pd.read_csv(sciezka_do_pliku)
    if data is not None:
        recent_data['Date'] = pd.to_datetime(recent_data['Date'], format='%Y-%m-%d', errors='coerce')
        data = pd.to_datetime(data)
        recent_data = recent_data[recent_data['Date'] < data].tail(20)
    else:
        recent_data = recent_data.tail(20)
        
    recent_data = recent_data[['Close', 'compound', 'likes', 'retweets']]
    recent_data = recent_data.values.astype('float32')
    recent_data = np.reshape(recent_data, (1, recent_data.shape[0], recent_data.shape[1]))
    X_recent = recent_data.copy()
    prediction = best_model.predict(X_recent)
    
    ifPumpDump = 0
    if prediction[0][0] < 0.15:
        ifPumpDump = 0
    elif prediction[0][0] < 0.3:
        ifPumpDump = 1
    else:
        ifPumpDump = 2
    return ifPumpDump


