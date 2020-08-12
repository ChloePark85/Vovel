import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db=client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://ko.wikisource.org/wiki/%EA%B8%88%EB%8F%84%EB%81%BC', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

story=soup.select("#mw-content-text > div.mw-parser-output > div > p")

text=""
for p_tag in story:
    text += p_tag.text

print(text)

lines = text.split("\n")

print(lines)

for line in lines:
    if line.startswith('“'):
        print (f"Chat: {line}")
    else:
        print (f"Narration: {line}")

#     doc ={
#         'narration':narration,
#         'chat':chat
#     }
#
#
# db.myproject.insert_one(doc)