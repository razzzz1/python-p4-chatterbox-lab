from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = Message.query.all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages/<int:id>')
def messages_by_id(id):
    message = Message.query.get(id)
    if not message:
        return '', 404
    return message.to_dict()

@app.route('/messages', methods=['POST'])
def create_new_message():
    body = request.json.get('body')
    username = request.json.get('username')
    message = Message(body=body, username=username)
    db.session.add(message)
    db.session.commit()
    response = make_response(message.to_dict(), 201)
    response.headers['Location'] = f'/messages/{message.id}'
    return response

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)
    if message:
        message.body = request.json.get('body', message.body)
        message.username = request.json.get('username', message.username)
        db.session.commit()
        return jsonify(message.to_dict()), 200
    else:
        return jsonify({"error": "Message not found"}), 404

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify(message.to_dict()), 200
    else:
        return jsonify({"error": "Message not found"}), 404


if __name__ == '__main__':
    app.run(port=5555)