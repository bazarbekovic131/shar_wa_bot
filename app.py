from flask import Flask, request, jsonify
from flask_cors import CORS
from db import WADatabase
import requests
import logging
logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

####### Conversation state tracking #########
user_states = {}
survey_questions = [
    "Возрастная группа: 1) 20-30, 2) 30-40",
    "Имели ли вы опыт работы на производстве: 1) да, 2) нет",
    "Если да, опыт работы: 1) менее 5 лет, 2) 5-10 лет, 3) 10-20 лет, 4) больше 20 лет",
    "Семейное положение: 1) в браке, 2) не в браке",
    "Имеются ли дети: 1) да, 2) нет"
]

################ DOC-V    ###################

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_id = data['id']
    message = data['message']
    user_phone_number = data['phone']

    # Send message via WhatsApp API
    send_whatsapp_message(user_phone_number, message)

    return jsonify({'status': 'Message sent'})

def send_whatsapp_message(to, message):
    # Replace with your actual API call to WhatsApp
    # Example using Twilio
    
    # account_sid = os.getenv('TWILIO_SID')
    # auth_token = os.getenv('TWILIO_TOKEN')
    # client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_= os.getenv('TWILIO_WA_NUMBER'),  # Your Twilio WhatsApp number
        to=f'whatsapp:{to}'
    )

@app.route('/test_send_message', methods = ['POST'])
def test_send_message():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')
    user_phone_number = data.get('phone')

    # Log the received data
    logging.info(f'Received message for {user_id} ({user_phone_number}): {message}')

    return jsonify({'status': 'Message logged', 'username': user_id, 'phone_number': user_phone_number, 'text': message})

############### HR Handler #################

@app.route('/whatsapp-form', methods = ['POST'])
def webhook():
    data = request.form
    from_number = data.get('from').replace('whatsapp:', '')
    message_body = data.get('body').strip()

    # Handle conversation flow
    if from_number not in user_states:
        # New user interaction
        if database.has_completed_survey(from_number):
            send_whatsapp_message(from_number, "Вы уже завершили опрос. Спасибо!")
        else:
            user_states[from_number] = {'question_index': 0, 'responses': []}
            send_whatsapp_message(from_number, survey_questions[0])
    else:
        # Existing user interaction
        state = user_states[from_number]
        if state['question_index'] < len(survey_questions):
            state['responses'].append(message_body)
            state['question_index'] += 1
            if state['question_index'] < len(survey_questions):
                send_whatsapp_message(from_number, survey_questions[state['question_index']])
            else:
                # Save survey responses and thank the user
                save_survey_responses(from_number, state['responses'])
                send_whatsapp_message(from_number, "Спасибо за участие в опросе. Свяжитесь с нами по телефону.")
                del user_states[from_number]

    return "OK", 200

def save_survey_responses(phone, responses):
    results = {
        'age_group': responses[0],
        'production_experience': responses[1],
        'experience_years': responses[2] if responses[1] == '1' else None,
        'marital_status': responses[3],
        'children_status': responses[4]
    }
    database.save_survey_results(phone, results)

if __name__ == '__main__':
    db_config = {
        'dbname': os.getenv('DBNAME'),
        'user': os.getenv('DBUSER'),
        'password': os.getenv('DBPASSWORD'),
        'host': os.getenv('DBHOST'),
        'port': os.getenv('DBPORT')
    }

    database = WADatabase(db_config)
    database.create_tables() # CREATE TABLES IF THEY DONT EXIST

    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_TOKEN')
    client = Client(account_sid, auth_token)

    app.run(port=5000)

