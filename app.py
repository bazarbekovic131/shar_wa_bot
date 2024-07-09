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

# Endpoint to handle HTTP requests from DOC-V
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_id = data['user_id']
    message = data['message']
    user_phone_number = data['phone']

    # Send message via WhatsApp API
    send_whatsapp_message(user_phone_number, message)

    return jsonify({'status': 'Message sent'})

def send_whatsapp_message(to, message):
    # Replace with your actual API call to WhatsApp
    # Example using Twilio
    

    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_TOKEN')
    client = Client(account_sid, auth_token)

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

if __name__ == '__main__':
    db_config = {
        'dbname': 'shark_whatsapp',
        'user': 'shark_whatsapp',
        'password': 'bazarbekovic',
        'host': 'localhost',
        'port': '5432'
    }

    database = WADatabase(db_config)

    app.run(port=5000)

