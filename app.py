from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Konfigurasi URI database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fuel.db'  # Gantilah dengan URI database Anda
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definisikan model Anda
class Predict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jarakTempuh = db.Column(db.Float, nullable=False)
    bahanBakar = db.Column(db.Float, nullable=False)
    merkKendaraan = db.Column(db.String(100), nullable=False)
    estimasiBensin = db.Column(db.Float, nullable=False)
    totalBiaya = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Buat tabel database
with app.app_context():
    db.create_all()

# Rute
@app.route('/predicts/new', methods=['POST'])
def create_predict():
    data = request.get_json()
    new_predict = Predict(
        jarakTempuh=data.get('jarakTempuh'),
        bahanBakar=data.get('bahanBakar'),
        merkKendaraan=data.get('merkKendaraan'),
        estimasiBensin=data.get('estimasiBensin'),
        totalBiaya=data.get('totalBiaya'),
        photo=data.get('photo')
    )
    db.session.add(new_predict)
    db.session.commit()
    return jsonify(new_predict.serialize()), 201

@app.route('/predicts', methods=['GET'])
def get_predicts():
    predicts = Predict.query.all()
    return jsonify([predict.serialize() for predict in predicts]), 200

@app.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify([article.serialize() for article in articles]), 200

@app.route('/articles/new', methods=['POST'])
def create_article():
    data = request.get_json()
    new_article = Article(
        title=data.get('title'),
        body=data.get('body'),
        photo=data.get('photo')
    )
    db.session.add(new_article)
    db.session.commit()
    return jsonify(new_article.serialize()), 201

# Metode serialisasi untuk model Anda
def serialize(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

Predict.serialize = serialize
Article.serialize = serialize

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
