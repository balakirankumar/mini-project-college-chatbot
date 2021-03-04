#import modules
from flask import Flask, render_template, request
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instancep
chatbot = ChatBot(
    'Buddy',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I am sorry, but I do not understand. I am still learning.',
        'maximum_similarity_threshold': 1.0
        }
    ],
    database_uri='sqlite:///database1999.sqlite3'
) 
# Training with personal Ques & Ans 
training_data_college = open('training_data/College.txt').read().splitlines()
training_data_gretting = open('training_data/grettings.txt').read().splitlines()
training_data_more = open('training_data/more.txt').read().splitlines()

#combining all data
training_data = training_data_college + training_data_gretting + training_data_more

trainer = ListTrainer(chatbot)
trainer.train(training_data) 
# Training with English Corpus Data 
trainer_corpus = ChatterBotCorpusTrainer(chatbot)

app = Flask(__name__)
app.static_folder = 'static'

    
@app.route("/")
def home():
    return render_template("Ngit.html")


@app.route("/bot")
def bot():
    return render_template("bot.html")
    
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    userText = userText.title()
    # print(userText)
    return str(chatbot.get_response(userText))


