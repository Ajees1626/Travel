from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

app = Flask(__name__)
CORS(app)

@app.route('/send', methods=['POST'])
def send_email():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    subject = data.get('subject')
    message = data.get('message')

    if not all([name, email, subject, message]):
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    email_message = EmailMessage()
    email_message['Subject'] = f"New Contact Message: {subject}"
    email_message['From'] = EMAIL_ADDRESS
    email_message['To'] = EMAIL_ADDRESS
    email_message.set_content(f"""
You have received a new message from your website contact form.

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
    """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(email_message)
        return jsonify({"success": True, "message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
