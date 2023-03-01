from flask import Flask, jsonify, request
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    if request.args.get("hub.mode") == "subscribe" and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == 'hello':
            return 'Verification token mismatch', 403
        print('hello', request.args['hub.challenge'])
        return request.args['hub.challenge'], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    # print(url_for('static', filename='video.mp4'))
    data = request.get_json()
    
    # typing_off()
    for entry in data['entry']:
        for messaging_event in entry['messaging']:
            
            sender_id = messaging_event['sender']['id']
            
            # typing_on(sender_id)
            if 'message' in messaging_event:
                if 'text' in messaging_event['message'] and 'quick_reply' not in messaging_event['message']:
                    query = messaging_event['message']['text']
                    print(query)

    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000),)
