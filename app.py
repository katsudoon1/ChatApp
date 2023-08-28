from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# 環境変数からAPIキーを読み込む
openai.api_key = os.environ.get('OPENAI_API_KEY')

messages = [
    {"role": "system", "content": "日本語で回答してください"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    messages.append({"role": "user", "content": user_input})

    print(f"messages: {messages}")  # デバッグ用に入力を出力

    model_name = "gpt-3.5-turbo"  # または任意のGPT-3.5モデル
    response = openai.ChatCompletion.create(model=model_name, messages=messages)

    print(f"API response: {response}")  # デバッグ用にAPIのレスポンスを出力

    chat_output = response.choices[0]['message']['content'].strip()
    messages.append({"role": "assistant", "content": chat_output})
    return jsonify({"chat_output": chat_output})

if __name__ == '__main__':
    app.run(debug=True)
