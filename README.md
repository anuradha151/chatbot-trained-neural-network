## Chatbot with Intent Recognition and Response Generation ##

This repository contains Python code for building a chatbot that can understand user intents and generate appropriate responses. It leverages the power of TensorFlow and natural language processing (NLP) techniques.

**Key Features:**

- **Intent Recognition:** Accurately classifies user input into predefined intents using a trained neural network model.
- **Response Generation:** Provides relevant responses based on the identified intent, drawing from a set of pre-defined responses.
- **Data-Driven Training:** Trains the model on a dataset of intents and patterns, enabling continuous improvement.

**Dependencies:**

- Python 3.x
- TensorFlow
- NumPy
- nltk
- pickle
- json

**Project Structure:**

- `intents.json`: Contains the dataset of intents and their corresponding patterns and responses.
- `words.pkl`: Stores the processed vocabulary of words used in the training data.
- `classes.pkl`: Stores the list of intent classes identified in the dataset.
- `chatbotmodel.keras`: The trained TensorFlow Keras model for intent classification.
- `training.py`: Script for training the chatbot model.
- `chatbot.py`: Script for interacting with the trained chatbot and generating responses.