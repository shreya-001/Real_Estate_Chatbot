from flask import Flask,render_template,request,jsonify
from transformers import AutoModelForCausalLM,AutoTokenizer
import torch

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
    return jsonify({"response" : response})

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


if __name__ ==  "__main__":
    app.run(debug=True)
