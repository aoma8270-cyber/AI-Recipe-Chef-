# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI()

# 1. CORS設定（Next.jsからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Geminiの設定
# ↓↓↓ ここにあなたのAPIキーを入れてください ↓↓↓
import os  

# Renderの設定画面に入力した「GEMINI_API_KEY」という値を読み込む
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 

genai.configure(api_key=GEMINI_API_KEY)
# モデルの準備 (gemini-1.5-flash は高速で無料枠も大きい)
# 最後に "-latest" をつけてみる
model = genai.GenerativeModel("gemini-2.0-flash")

class ChatRequest(BaseModel):
    message: str
    style: str

# 3. APIエンドポイント
# 3. APIエンドポイント
@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
       # ▼▼▼ プロンプトをアフィリエイト仕様に変更 ▼▼▼
        system_prompt = f"""
        あなたは三ツ星レストランのシェフです。
        ユーザーが持っている食材：【 {req.message} 】
        希望する料理のジャンル：【 {req.style} 】

        上記をもとに、最適なレシピを1つ提案してください。
        材料と手順を明確にし、美味しく作るコツをアドバイスしてください。

        ■最後に
        この料理を作るのに「あると便利な調理器具」または「こだわると美味しい食材」を1つだけピックアップし、
        「おすすめアイテム: [アイテム名]」と出力した後に、
        そのアイテムの Amazon検索URL (https://www.amazon.co.jp/s?k=[アイテム名]&tag=recipechef01-22) を表示してください。
        """
        # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

        response = model.generate_content(system_prompt)
        
        return {"reply": response.text}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "エラーが発生しました。コンソールを確認してください。"}