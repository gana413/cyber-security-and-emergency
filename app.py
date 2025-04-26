from flask import Flask, request, jsonify
import flask
from flask_cors import CORS # type: ignore
from twilio.rest import Client # type: ignore

app = Flask(__name__)
CORS(app)

# మీ Twilio ఖాతా SID మరియు Auth టోకెన్ ఇక్కడ ఉంచండి
account_sid = "AC2babd085ee2d96f9d9f76517e94744f7"  # మీ ఖాతా SID ని ఇక్కడ ఉంచండి
auth_token = "your_auth_token"  # మీ Auth టోకెన్‌ను ఇక్కడ ఉంచండి
client = Client(account_sid, auth_token)

# మీ Twilio ఫోన్ నెంబర్‌ను ఇక్కడ ఉంచండి
twilio_phone_number = "+17753682698"  # మీ Twilio ఫోన్ నెంబర్‌ను ఇక్కడ ఉంచండి

def send_sms(to_phone_number, message):
    try:
        message = client.messages.create(
            to=to_phone_number,
            from_=twilio_phone_number,
            body=message
        )
        print(f"SMS పంపబడింది: {to_phone_number} -> {message.sid}")
        return True
    except Exception as e:
        print(f"SMS పంపడంలో లోపం: {e}")
        return False

# WhatsApp పంపడానికి కూడా ఇలాంటి లాజిక్ ఉంటుంది, కానీ WhatsApp Business API సెటప్ అవసరం
def send_whatsapp(to_phone_number, message):
    try:
        message = client.messages.create(
            to=f"whatsapp:{to_phone_number}",
          from_=twilio_phone_number,
            body=message
        )
        print(f"SMS పంపబడింది: {to_phone_number} -> {message.sid}")
        return True
    except Exception as e:
        print(f"SMS పంపడంలో లోపం: {e}")
        return False

# WhatsApp పంపడానికి కూడా ఇలాంటి లాజిక్ ఉంటుంది, కానీ WhatsApp Business API సెటప్ అవసరం
def send_whatsapp(to_phone_number, message):
    try:
        message = client.messages.create(
            to=f"whatsapp:{to_phone_number}",
            from_=f"whatsapp:{twilio_phone_number}",
            body=message
        )
        print(f"WhatsApp పంపబడింది: {to_phone_number} -> {message.sid}")
        return True
    except Exception as e:
        print(f"WhatsApp పంపడంలో లోపం: {e}")
        return False

@app.route('/send_sos', methods=['POST'])
def send_sos_endpoint():
    data = request.get_json()
    contacts = data.get('contacts', [])
    message = data.get('message', '')

    for contact in contacts:
        send_sms(contact, message)
        send_whatsapp(contact, message) # WhatsApp పంపడానికి అదనపు సెటప్ మరియు ఆమోదం అవసరం

      return jsonify({'status': 'success', 'message': 'SOS సందేశాలు పంపబడ్డాయి'})

@app.route('/report_problem', methods=['POST'])
def report_problem_endpoint():
    data = request.get_json()
    problem = data.get('problem', '')
    print(f"సమస్య నివేదించబడింది: {problem}")
    return jsonify({'status': 'success', 'message': 'సమస్య నివేదిక స్వీకరించబడింది'})

if __name__ == '_main_':
    app.run(debug=True)
