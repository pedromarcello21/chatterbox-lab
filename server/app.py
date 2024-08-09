from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import Message

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
    messages = Message.query.order_by(Message.created_at).all()
    return [message.to_dict() for message in messages], 200

@app.route('/messages/<int:id>')
def messages_by_id(id):
    message_found = Message.query.where(id == Message.id).first()
    return message_found.to_dict(), 200

@app.post('/messages')
def create_message():
    data = request.json
    if data:
        new_message = Message(**data)
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201
    else:
        {'error', 'invalid message'}

@app.patch('/messages/<int:id>')
def update_message(id):
    data = request.json
    found_message = Message.query.where(id==Message.id).first()
    found_message.body = data['body']
    db.session.commit()
    return found_message.to_dict(), 200

@app.delete('/messages/<int:id>')
def delete_message(id):
    message_to_delete = Message.query.where(id==Message.id).first()
    db.session.delete(message_to_delete)
    db.session.commit()
    return {}, 200

if __name__ == '__main__':
    app.run(port=5555)
