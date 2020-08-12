from flask import Flask, render_template, url_for, jsonify, request, redirect
import translate, recognize, keywords
from werkzeug.utils import secure_filename
import os

app = Flask('__name__')

@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static\\uploads',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('index.html')

@app.route('/speech_recognizer', methods=['POST'])
def speech_recognizer():
    data = request.get_json()
    audio_filename = 'static/uploads/' + data['filename']
    language = data['language']
    response = recognize.get_recognizer(audio_filename, language)
    print(response)
    print(jsonify(response))
    return response

@app.route('/speech_translator', methods=['POST'])
def speech_translator():
    data = request.get_json()
    text_input = data['text']
    translation_output = data['to']
    response = translate.get_translation(text_input, translation_output)
    return jsonify(response)

@app.route('/keywords_extract', methods=['POST'])
def keywords_extract():
    data = request.get_json()
    input_text = data['inputText']
    input_lang = data['inputLanguage']
    response = keywords.get_keyphrases(input_text, input_lang)
    return jsonify(response)

app.run(debug = True)