from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client= MongoClient('localhost', 27017)
db=client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

#사용자가 텍스트 파일을 올리면 파일을 읽어서 채팅과 나레이션으로 구분하고 db에 저장함.
@app.route('/storydata', methods=["POST"])
def post_storydata():
    storydata = request.files['text_file']
    print(type(storydata))
    print(storydata.read())
    lines = storydata.split("\n")
    for index, line in enumerate(lines):
        if line.startswith('"'):
            line_type = "chat"
            # print(f"Chat: {line}")
        else:
            line_type = "narration"
            # print(f"Narration: {line}")
    doc = {
        'order': index,
        'type': line_type,
        'text': line,
    }
    db.myproject.insert_one(doc)
    return jsonify({'result':'success', 'storylines':storydata, 'msg':'스토리가 업로드되었습니다'})

#db에 저장된 데이터를 가져와서 json으로 변환된 것을 html에 전달함.
@app.route('/storytransform', methods=["GET"])
def show_storydata():
    storydata= list(db.myproject.find({}, {'_id':0}))
    return jsonify({'result':'success', 'type': line_type, 'text': line})




# @app.route('/api/show', methods= ['GET'])
# def show_story():
#     story=list(db.myproject.find({}, {'_id':False}))
#     return jsonify({'result': 'success', 'storylines': story})

# @app.route('/api/transform', methods= ['GET'])
# def show_chatify():
#     return jsonify({'result': 'success', 'msg': '스토리를 변환했습니다.'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

    # name = request.args.get('name')
    # return render_template('detail.html', name = name)