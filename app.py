from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
db = SQLAlchemy(app)

class ButtonPress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    button_value = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'button_value': self.button_value,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

with app.app_context():
    db.create_all()

@app.route('/button', methods=['POST'])
def receive_button():
    data = request.json
    press = ButtonPress(button_value=data['value'])
    db.session.add(press)
    db.session.commit()
    print(f"✅ Button {data['value']} pressed at {datetime.utcnow()}")
    return jsonify({'status': 'saved'}), 200

@app.route('/data', methods=['GET'])
def get_data():
    presses = ButtonPress.query.order_by(ButtonPress.timestamp.desc()).all()
    return jsonify([p.to_dict() for p in presses])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
