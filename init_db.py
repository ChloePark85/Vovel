import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db=client.dbsparta


text=""
for p_tag in story:
    text += p_tag.text

# print(text)

lines = text.split("\n")

# print(lines)

def get_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://ko.wikisource.org/wiki/%EA%B8%88%EB%8F%84%EB%81%BC', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    story = soup.select("#mw-content-text > div.mw-parser-output > div > p")


for index, line in enumerate(lines):
    if line.startswith('“'):
        line_type = "chat"
        print (f"Chat: {line}")
    else:
        line_type = "narration"
        print (f"Narration: {line}")

    doc ={
        'order': index,
        'type': line_type,
        'text': line,
    }


db.myproject.insert_one(doc)