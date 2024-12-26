from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Contoh data
predicts = []
articles = []

@app.route('/predict/new', methods=['POST'])
def create_predict():
    data = request.get_json()
    new_predict = {
        'id': len(predicts) + 1,
        'jarakTempuh': data.get('jarakTempuh'),
        'bahanBakar': data.get('bahanBakar'),
        'merkKendaraan': data.get('merkKendaraan'),
        'estimasiBensin': data.get('estimasiBensin'),
        'totalBiaya': data.get('totalBiaya'),
        'photo': data.get('photo'),
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    predicts.append(new_predict)
    return jsonify(new_predict), 201

@app.route('/predict', methods=['GET'])
def get_predicts():
    return jsonify(predicts), 200

@app.route('/articles', methods=['GET'])
def get_articles():
    return jsonify(articles), 200

@app.route('/articles/new', methods=['POST'])
def create_article():
    data = request.get_json()
    new_article = {
        'id': len(articles) + 1,
        'title': data.get('title'),
        'body': data.get('body'),
        'photo': data.get('photo'),
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    articles.append(new_article)
    return jsonify(new_article), 201

if __name__ == '__main__':
    app.run(debug=True)
