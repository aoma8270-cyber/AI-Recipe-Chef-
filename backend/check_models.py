# backend/check_models.py
import google.generativeai as genai

# ↓↓↓ あなたのAPIキーを入れてください ↓↓↓
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)

print("--- 使えるモデルの一覧 ---")
try:
    for m in genai.list_models():
        # "generateContent"（チャット機能）に対応しているモデルだけ表示
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    print("------------------------")
except Exception as e:
    print(f"エラー: {e}")