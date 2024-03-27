import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from bs4 import BeautifulSoup


app = Flask(__name__)
model = pickle.load(open('spam-email-classifier', 'rb'))
vectorizer = pickle.load(open('vectorizer', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        text = request.form['text']

        if len(text.strip()) == 0:
            return render_template('index.html', prediction_text='Please Enter The Text!')
           
        elif len(text.strip()) <= 25:
            return render_template('index.html', prediction_text='Text is too short!')
        
        else:
            cleaned_text = []
            cleaned_text.append(clean_message(text))
            vector_data = vectorizer.transform(cleaned_text)
            print(type(vector_data))
            prediction = model.predict(vector_data)
            predict_percentage = model.predict_proba(vector_data)[0]
            not_spam = predict_percentage[0]*100
            spam = predict_percentage[1]*100
            result = ''
            if prediction[0] == 1:
                result = 'Spam'
            else:
                result = 'Not Spam'

            print(prediction[0])
            print(result)
            
            return render_template('index.html', prediction_text=f'Email is {result}', 
                                                 spam_percentage=f'{spam:.2f} %',
                                                 not_spam_percentage=f'{not_spam:.2f} %')

       

def clean_message(message, stop_words=set(stopwords.words('english'))):
    '''
    Takes the message(email body) and performs operations 
    like tokenising, converting to lowercase, removing stop words
    and punctuation and HTML tags
    
    message: email body
    '''
    # remove HTML tags
    soup = BeautifulSoup(message, 'html.parser')
    message = soup.get_text()
    
    # tokenize the words & convert to lower
    words = word_tokenize(message.lower())
    
    filtered_words = []
    for word in words:
        # Removes stop words & punctuation
        if word not in stop_words and word.isalpha():
            filtered_words.append(word)
    
    return ' '.join(filtered_words)

    

if __name__ == '__main__':
    app.run(debug=True)
