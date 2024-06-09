import json
import pickle
import numpy as np
import nltk

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from sqlalchemy.orm import Session

from repository import find_by_tag
from schemas import ChatResponse



lemmatizer = WordNetLemmatizer()
# TODO - remove intents.json usage for model training. Use db approach
# intents = json.loads(open('resources/intents.json').read())

words = pickle.load(open('generated/words.pkl', 'rb'))
classes = pickle.load(open('generated/classes.pkl', 'rb'))
# The output will be numerical data
model = load_model('generated/chatbotmodel.keras')


def deploy_model():

    global intents
    global words
    global classes
    global model

    intents = json.loads(open('resources/intents.json').read())
    words = pickle.load(open('generated/words.pkl', 'rb'))
    classes = pickle.load(open('generated/classes.pkl', 'rb'))
    # The output will be numerical data
    model = load_model('generated/chatbotmodel.keras')

# Clean up the sentences


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Converts the sentences into a bag of words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    # bow: Bag Of Words, feed the data into the neural network
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]  # res: result. [0] as index 0
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        print('r: ', r)
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(db: Session, tag: str ):
    db_intent = find_by_tag(db, tag=tag)
    return ChatResponse(
        response_text=db_intent.response_text,
        response_links=[link.url for link in db_intent.response_links]
    )

    # TODO - remove intents.json usage for model training. Use db approach
    # tag = intents_list[0]['intent']
    # list_of_intents = intents['intents']
    # for i in list_of_intents:
    #     if i['tag'] == tag:
    #         result = random.choice(i['responses'])
    #         break
    # return result


def chat(message, db: Session):
    intents_list = predict_class(message)
    return get_response(db, intents_list[0]['intent'])
