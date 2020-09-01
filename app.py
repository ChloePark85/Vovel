from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


# 서버에서 책 목록을 가져옴
@app.route('/bookList', methods=["GET"])
def read_book_list():
    book_list = list(db.bookList.find({}, {'_id': 0}))
    return jsonify({
        'result': 'success',
        'bookList': book_list
    })


# 책 정보를 쿼리 스트링으로 받아옴.
@app.route('/book', methods=["GET"])
def book_get():
    title_receive = request.args.get('title_give')
    book = db.bookList.find_one({"title": title_receive}, {"_id": 0})
    return jsonify({'result': 'success', 'book': book})


# 채팅형태로 변환해서 데이터베이스에 저장
@app.route('/makeStory', methods=['POST'])
def write_story():
    title = request.form['title']
    author = request.form['author']
    story = request.form['story']

    lines = story.split("\n")

    story = []

    for index, line in enumerate(lines):
        if line.startswith('"'):
            line_type = "chat"
            # print(f"Chat: {line}")
        else:
            line_type = "narration"
            # print(f"Narration: {line}")

        # Tutor: 대사 혹은 나레이션은 순서와 함께 하나의 content dictionary에 담습니다.
        content = {
            'order': index,
            'type': line_type,
            'text': line,
        }
        # Tutor: story 라는 list에 content를 담습니다. story => [<content>, <content>, <content>, ...]
        story.append(content)

    book = {
        'title': title,
        'author': author,
        'story': story,
    }
    db.bookList.insert_one(book)
    return jsonify({'result': 'success', 'msg': '스토리가 업로드되었습니다'})


# db에 저장된 데이터를 가져와서 json으로 변환된 것을 html에 전달함.
@app.route('/chatify', methods=["GET"])
def read_story():
    storylines = list(db.story.find({'story'}, {'_id': 0}))
    return jsonify({'result': 'success', 'storylines': storylines})


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
