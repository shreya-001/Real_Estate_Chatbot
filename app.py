from flask import Flask,render_template,request,jsonify
from transformers import AutoModelForCausalLM,AutoTokenizer,BartForConditionalGeneration
import torch
import requests
import nltk
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import re



from nltk.sentiment import SentimentIntensityAnalyzer

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# naming the flask apk
app = Flask(__name__)


# setting home page
@app.route("/")
def index():
    return render_template('chat.html')
    # return "Hello World!"


#sending and getting response from the chatbot.
#to update anything on server
@app.route("/get",methods = ["GET","POST"])
#now taking input from the html file



def chat():
    #getting msg field from the html file
    msg = request.form["msg"]
    #now passing the msg into other function
    input = msg
    response = get_Chat_response(input)
    
    response_bool = analyze_response(response)
    print(response_bool,'response_bool')
    if response_bool == False:
       return query_google_search_api(input)
    
    return response

def get_Chat_response(text):
    #taking chatbot code
    #https://huggingface.co/microsoft/DialoGPT-medium
    
    # Let's chat for 5 lines
    for step in range(5):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        #we already got the response.
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token,return_tensors = 'pt')
        
        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids,new_user_input_ids],dim = -1) if step > 0 else new_user_input_ids
        
        # generated a response while limiting the total chat history to 1000 tokens,
        chat_history_ids = model.generate(bot_input_ids,max_length = 1000,pad_token_id = tokenizer.eos_token_id)
        
        # pretty print last ouput tokens from bot
        return tokenizer.decode(chat_history_ids[:,bot_input_ids.shape[-1]:][0],skip_special_tokens = True)







def analyze_response(response):
  # Sentiment analysis
  sia = SentimentIntensityAnalyzer()

    # Topic modeling
  vectorizer = TfidfVectorizer()
  topic_model = MultinomialNB()

    # Keyword detection
  PUNT_KEYWORDS = ["I'm not sure", "I don't have enough information", "That's a great question, but","I'm unable"]


  # Sentiment analysis
  sentiment_score = sia.polarity_scores(response)["compound"]
  if sentiment_score < 0.0:
    return False

#   # Topic modeling
#   query_topic = topic_model.predict(vectorizer.transform([response]))[0]
#   response_topic = topic_model.predict(vectorizer.transform([response]))[0]
#   if query_topic != response_topic:
#     return False

  # Keyword detection
  for keyword in PUNT_KEYWORDS:
    if keyword in response:
      return False

  return True



def query_google_search_api(query):
    # Set up Google Search API credentials and parameters
    
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
    "key": "AIzaSyDC71vdmwP6WWmaIbxQ4YGf90Ydy3EeTPg",
    "cx": "c50cdabe0ed3a48e9",
    "q": query,
    "fullText": True,
    "maxSnippetLength": 500
    }

    response = requests.get(url, params=params)
    # Parse the response and return the top result
    result = response.json()["items"][0]["snippet"]
    print(result,'before rewriting')
    result=rewrite_response(result)
    print(result,'afterrewriting')
    return result

def rewrite_response(response):

    # Load the pre-trained language model
    model =BartForConditionalGeneration.from_pretrained('facebook/bart-base')
    date_pattern = r'^\w{3} \d{1,2}, \d{4}'
    response = re.sub(date_pattern, '', response)

    # Generate a rewritten response with a more conversational tone
    rewritten_response = rewritten_response = tokenizer.decode(model.generate(tokenizer.encode(response, return_tensors='pt'), max_length=100, temperature=1.5)[0], skip_special_tokens=True)

    print(rewritten_response,'rewritten')
    return response

if __name__ ==  "__main__":
    app.run(debug=True)
