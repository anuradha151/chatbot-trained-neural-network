import random
import json
import pickle
import numpy as np

import nltk
nltk.download('punkt')
nltk.download('wordnet')


#WordNetLemmatizer reduce the word to stem so that it wont loose performance

from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


def train():
    lemmatizer = WordNetLemmatizer()

    intents = json.loads(open('intents.json').read())
    #reading the json file as text


    #create 3 empty lists
    words = []
    classes = []
    documents = []
    ignore_letters = ['?', '!', '.', ',']


    ''' 
    How it works?:

    Look inside the intents in the json file and through the patterns. Then,
    append the words into the word list.
    '''
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # tokenize = splits up sentences into words
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            #(word_list) is a tuple. Tuple: stores multiple items into a single variable
            #(word_list) belongs to the category intent['tag']
            documents.append((word_list, intent['tag']))

            #check if the class is in the classes list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
    words = sorted(set(words))

    classes = sorted(set(classes))

    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))


    training = []
    output_empty = [0] * len(classes)

    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    max_length = max(len(x) for x, y in training)

    for i, (x, y) in enumerate(training):
        if len(x) < max_length: 
            training[i] = (x + [0] * (max_length - len(x)), y)
        if len(y) < max_length: 
            training[i] = (y + [0] * (max_length - len(y)), x)
    
    random.shuffle(training)
    training = np.array(training)

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    model = Sequential() # sequential model
    # 128 = Neurons  input_shape dependant on  the size of the training data of train_x
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    '''
    model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
    model.save('chatbot_model.model')
    '''

    hist = model.fit(np.array(train_x), np.array(train_y), epochs = 200, batch_size=5, verbose=1)
    model.save('chatbotmodel.h5', hist) #save the training data into a h5 file... I think?
    return {"message": "model trained"}