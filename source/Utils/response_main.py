from flask import Flask, request, render_template,jsonify
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from Utils.extract_entities import extract_entities
from Utils.filter_properties import filter_properties
from Utils.llama_response import fine_tuned_resp
from Utils.answer_composition import RealEstateChatbot


# Load the trained model
model = joblib.load('/home/jyotsna/Virtual_Real_Estate_Agent/model/new/new_lstm_model.pkl')
#model = load_model('model/new/lstm_model.h5')

# Load tokenizer and label encoder
tokenizer = joblib.load('/home/jyotsna/Virtual_Real_Estate_Agent/model/new/new_lsmt_tokenizer.pkl')
le = joblib.load('/home/jyotsna/Virtual_Real_Estate_Agent/model/new/new_lstm_label_encoder.pkl')

# Define the maximum sequence length
max_sequence_length = 9  # Adjust according to your training

property_df = pd.read_csv('/home/jyotsna/Virtual_Real_Estate_Agent/database/new_realtor_dataset.csv')

# Initialize the RealEstateChatbot
chatbot = RealEstateChatbot(filter_properties_func=filter_properties)


def predict(prompt):
    # Get the user input from the form
    user_input=prompt
    # # Preprocess the input
    new_sequence = tokenizer.texts_to_sequences([user_input])
    new_padded_sequence = pad_sequences(new_sequence, maxlen=max_sequence_length, padding='post')

    # #Predict the intent
    prediction = model.predict(new_padded_sequence)
    predicted_intent = np.argmax(prediction)
    
    # # Decode the predicted intent
    predicted_intent_array = np.array([predicted_intent])
    predicted_intent_label = le.inverse_transform(predicted_intent_array)[0]

    if predicted_intent_label=='google_search' : 
        response=fine_tuned_resp(user_input)
        return response
        
        
    try:
        # Extract entities from the user input
        entities = extract_entities(user_input)

        # Generate a response based on the predicted intent and extracted entities
        response = chatbot.compose_answer(predicted_intent_label, entities, property_df)

    except Exception as e:
        # If an exception occurs, try using the fine-tuned model
        response = fine_tuned_resp(user_input)
        if len(response)<2:
            response= "I'm unable to answer this at the momemt."

   


    # Return the prediction to the user
    #return render_template('index.html', prediction=predicted_intent_label,response = response)
    # Return the prediction and response to the user as JSON
    return response

