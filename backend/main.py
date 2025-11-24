# backend/main.py
import json
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

# generation_config を追加して JSONモードにする
model = genai.GenerativeModel(
    "gemini-2.0-flash",
    generation_config={"response_mime_type": "application/json"}
)

class ChatRequest(BaseModel):
    message: str
    style: str

# 3. APIエンドポイント
# 3. APIエンドポイント
@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        # プロンプト：JSON形式で返すように厳格に指定
        system_prompt = f"""
        あなたは三ツ星レストランのシェフです。
        ユーザーの食材：{req.message}
        希望ジャンル：{req.style}

        以下の情報をJSON形式で出力してください。
        キー名は必ず以下のようにしてください：
        - "content": レシピの本文（タイトル、材料、手順、コツ、Amazonリンクの案内まで含める）
        - "ingredients": この料理に必要な【すべての材料と調味料】のリスト（ユーザーが入力していないものも含む）

        レシピ本文の最後には、前回同様に調理器具のAmazonリンク案内も含めてください。
        """

        response = model.generate_content(system_prompt)
        
        # AIからの返事（JSON文字列）をPythonの辞書データに変換
        response_data = json.loads(response.text)
        
        # フロントエンドに返す（本文と、材料リストを別々に送る）
        return {
            "reply": response_data["content"],
            "ingredients": response_data["ingredients"]
        }
    
    except Exception as e:
        print(f"Error: {e}")
        # エラー時は空のリストを返す
        return {"reply": "エラーが発生しました。", "ingredients": []}