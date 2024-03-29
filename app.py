import streamlit as st
import pickle
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.data.path.append("/path/to/nltk_data")

from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
ps = PorterStemmer() #porterstemmer object

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("SMS Classifier")

input_sms = st.text_area("Enter the message")



def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text :
        if i not in stopwords.words('english') and i not in string.punctuation :
            y.append(i)
    
    text = y[:]
    y.clear()
    
    for i in text :
        y.append(ps.stem(i))
    
    # convert to a string
    return  " ".join(y)


if st.button('Predict'):

  # 1. preprocess

  transform_sms = transform_text(input_sms)

  # 2. vectorize

  vector_input = tfidf.transform([transform_sms])

  # 3. predict

  result = model.predict(vector_input)[0]

  # 4. display

  if result == 1 :
      st.header("Spam")
  else:
      st.header("Not spam")