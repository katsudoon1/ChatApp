from flask import Flask, render_template, request, jsonify, session
from uuid import uuid4
import openai
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
session_messages = {}

# 環境変数からAPIキーを読み込む
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/')
def index():
    # ユニークなセッションIDを作る
    session_id = str(uuid4())
    session['session_id'] = session_id

    #このセッションのmessagesを初期化
    session_messages[session_id] = [{"role": "system", "content": "日本語で回答してください"}]
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    session_id = session.get('session_id')
    if session_id is None:
        return jsonify({"error": "Session ID is missing"}), 400
    
    user_input = request.json.get('user_input')
    session_messages[session_id].append({"role": "user", "content": user_input})

    print(f"session_messages: {session_messages[session_id]}")  # デバッグ用に入力を出力

    model_name = "gpt-3.5-turbo"  # または任意のGPT-3.5モデル
    response = openai.ChatCompletion.create(model=model_name, messages=session_messages[session_id])

    print(f"API response: {response}")  # デバッグ用にAPIのレスポンスを出力

    chat_output = response.choices[0]['message']['content'].strip()
    session_messages[session_id].append({"role": "assistant", "content": chat_output})
    return jsonify({"chat_output": chat_output})

if __name__ == '__main__':
    app.run(debug=True)
