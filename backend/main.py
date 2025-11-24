from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
import json

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Geminiの設定
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# JSONモードを有効化
model = genai.GenerativeModel(
    "gemini-2.0-flash",
    generation_config={"response_mime_type": "application/json"}
)

class ChatRequest(BaseModel):
    message: str
    style: str

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        # プロンプト
        system_prompt = f"""
        あなたは三ツ星レストランのシェフです。
        ユーザーの食材：{req.message}
        希望ジャンル：{req.style}

        以下の情報をJSON形式で出力してください。
        キー名は必ず以下のようにしてください：
        - "content": レシピの本文（タイトル、材料、手順、コツ、Amazonリンクの案内まで含める）
        - "ingredients": この料理に必要な【すべての材料と調味料】のリスト（ユーザーが入力していないものも含む）

        レシピ本文の最後には、前回同様に調理器具のAmazonリンク案内も含めてください。
        （URLには &tag=recipechef01-22 をつけてください）
        """

        response = model.generate_content(system_prompt)
        
        # ★★★ ここが修正ポイント（クリーニング処理） ★★★
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        
        # きれいになったテキストを読み込む
        response_data = json.loads(clean_text)
        
        return {
            "reply": response_data["content"],
            "ingredients": response_data["ingredients"]
        }
    
    except Exception as e:
        # エラーが起きたら、ログに詳細を出す
        print(f"Error detail: {e}")
        # AIの生の返答もログに出して確認できるようにする
        try:
            print(f"Raw AI response: {response.text}")
        except:
            pass
            
        return {"reply": "エラーが発生しました。しばらく待ってから再試行してください。", "ingredients": []}