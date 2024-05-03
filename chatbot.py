import random
import json
import pickle
import numpy as np

import nltk
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

def chat():

    intents = json.loads(open('intents.json').read())
    return intents