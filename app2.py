from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Predict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jarakTempuh = db.Column(db.Float, nullable=False)
    bahanBakar = db.Column(db.String(50), nullable=False)
    merkKendaraan = db.Column(db.String(50), nullable=False)
    estimasiBensin = db.Column(db.Float, nullable=False)
    totalBiaya = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@app.route('/predict', methods=['POST'])
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
    return jsonify(new_predict), 201

@app.route('/predict', methods=['GET'])
def get_predicts():
    predicts = Predict.query.all()
    result = [{
        'id': predict.id,
        'jarakTempuh': predict.jarakTempuh,
        'bahanBakar': predict.bahanBakar,
        'merkKendaraan': predict.merkKendaraan,
        'estimasiBensin': predict.estimasiBensin,
        'totalBiaya': predict.totalBiaya,
        'photo': predict.photo,
        'createdAt': predict.createdAt,
        'updatedAt': predict.updatedAt
    } for predict in predicts]
    return jsonify(result), 200

@app.route('/articles', methods=['POST'])
def create_article():
    data = request.get_json()
    new_article = Article(
        title=data.get('title'),
        body=data.get('body'),
        photo=data.get('photo')
    )
    db.session.add(new_article)
    db.session.commit()
    return jsonify(new_article), 201

@app.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    result = [{
        'id': article.id,
        'title': article.title,
        'body': article.body,
        'photo': article.photo,
        'createdAt': article.createdAt,
        'updatedAt': article.updatedAt
    } for article in articles]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
