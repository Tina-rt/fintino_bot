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


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000),)
