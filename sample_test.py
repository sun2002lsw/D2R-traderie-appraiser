from html_builder import *
import webbrowser
import json
import os


# 원래는 DB에서 읽어올 데이터
sample_data_path = './sample_data.txt'
with open(sample_data_path, 'r', encoding='utf-8') as file:
    sample_data = file.read()

db_data = json.loads(sample_data)
for idx, data in enumerate(db_data):
    db_data[idx]['ItemValues'] = json.loads(data['ItemValues'])

# AWS lambda에서 사용될 함수
html = build_html(db_data)

# 결과를 파일로 만들어서 실행해 본다
sample_result_path = './sample_result.html'
with open(sample_result_path, 'w', encoding='utf-8') as file:
    file.write(html)

sample_result_abspath = os.path.abspath(sample_result_path)
webbrowser.open('file://' + sample_result_abspath)