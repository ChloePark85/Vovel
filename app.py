from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client= MongoClient('localhost', 27017)
db=client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/show', methods= ['GET'])
def show_story():
    story=list(db.myproject.find({}, {'_id':False}))
    return jsonify({'result': 'success', 'storylines': story})

# @app.route('/api/transform', methods= ['GET'])
# def show_chatify():
#     return jsonify({'result': 'success', 'msg': '스토리를 변환했습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

    # name = request.args.get('name')
    # return render_template('detail.html', name = name)