# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI()

# 1. CORS設定（Next.jsからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Geminiの設定
# ↓↓↓ ここにあなたのAPIキーを入れてください ↓↓↓
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)

# モデルの準備 (gemini-1.5-flash は高速で無料枠も大きい)
# 最後に "-latest" をつけてみる
model = genai.GenerativeModel("gemini-2.0-flash")

class ChatRequest(BaseModel):
    message: str

# 3. APIエンドポイント
# 3. APIエンドポイント
@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        # ▼▼▼ レシピ提案AIのプロンプト ▼▼▼
        system_prompt = f"""
        あなたは三ツ星レストランのシェフです。
        ユーザーが入力した「冷蔵庫にある食材」を使って作れる、簡単で美味しいレシピを1つだけ提案してください。
        材料と手順を箇条書きで分かりやすく提示し、最後に「美味しく作るコツ」をワンポイントアドバイスしてください。
        食材: {req.message}
        """
        # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

        response = model.generate_content(system_prompt)
        
        return {"reply": response.text}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "エラーが発生しました。コンソールを確認してください。"}