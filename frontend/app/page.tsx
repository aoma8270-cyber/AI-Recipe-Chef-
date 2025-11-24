// frontend/src/app/page.tsx
"use client";

import { useState, useEffect } from "react";

// 保存するデータの形を定義（型定義）
type SavedRecipe = {
  title: string;
  content: string;
  date: string;
};

export default function Home() {
  // --- 状態管理 (State) ---
  const [input, setInput] = useState("");
  const [style, setStyle] = useState("おまかせ");
  const [reply, setReply] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  
  // 保存したレシピを入れるリスト（文字列ではなく、オブジェクトの配列にする）
  const [savedRecipes, setSavedRecipes] = useState<SavedRecipe[]>([]);

  // --- 1. アプリ起動時に保存データを読み込む ---
  useEffect(() => {
    const saved = localStorage.getItem("myRecipes");
    if (saved) {
      setSavedRecipes(JSON.parse(saved));
    }
  }, []);

  // --- 2. レシピを送信してAIに聞く ---
  const handleSend = async () => {
    if (!input) return;
    setIsLoading(true);
    try {
      const response = await fetch("https://ai-recipe-backend-6duc.onrender.com/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, style: style }),
      });
      const data = await response.json();
      setReply(data.reply);
    } catch (error) {
      console.error(error);
      setReply("エラーが発生しました。");
    } finally {
      setIsLoading(false);
    }
  };

  // --- 3. タイトルをつけてレシピを保存する ---
  const handleSave = () => {
    if (!reply) return;

    // ポップアップでタイトルを入力させる
    const title = window.prompt("レシピにタイトルをつけてください", "今日の料理");
    
    // キャンセルされたら保存しない
    if (!title) return;

    // 新しいレシピデータを作る
    const newRecipe: SavedRecipe = {
      title: title,
      content: reply,
      date: new Date().toLocaleDateString(), // 今日の日付
    };

    // リストに追加して保存
    const newList = [newRecipe, ...savedRecipes];
    setSavedRecipes(newList);
    localStorage.setItem("myRecipes", JSON.stringify(newList));
    
    alert(`「${title}」を保存しました！`);
  };

  // --- 4. 保存したレシピを削除する ---
  const handleDelete = (index: number) => {
    if(!window.confirm("本当に削除しますか？")) return;
    
    const newList = savedRecipes.filter((_, i) => i !== index);
    setSavedRecipes(newList);
    localStorage.setItem("myRecipes", JSON.stringify(newList));
  };

  return (
    <main className="min-h-screen bg-orange-50 p-8 text-gray-800">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold mb-6 text-center text-orange-600">
          AIレシピシェフ 👨‍🍳
        </h1>
        
        {/* --- 入力エリア --- */}
        <div className="bg-white p-6 rounded-xl shadow-md mb-8">
          <label className="block mb-2 font-bold">冷蔵庫にある食材</label>
          <textarea
            className="w-full p-3 border rounded-lg mb-4 h-24"
            placeholder="例: 卵、牛乳、キャベツ"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />

          <label className="block mb-2 font-bold">食べたいジャンル</label>
          <select
            className="w-full p-3 border rounded-lg mb-6"
            value={style}
            onChange={(e) => setStyle(e.target.value)}
          >
            <option value="おまかせ">おまかせ</option>
            <option value="和食">和食</option>
            <option value="洋食">洋食</option>
            <option value="中華">中華</option>
            <option value="イタリアン">イタリアン</option>
            <option value="時短">時短料理</option>
          </select>

          <button
            className="w-full bg-orange-500 text-white p-4 rounded-lg font-bold text-lg hover:bg-orange-600 transition disabled:bg-gray-300"
            onClick={handleSend}
            disabled={isLoading}
          >
            {isLoading ? "シェフが考案中..." : "レシピを考えて！"}
          </button>
        </div>

        {/* --- AIの回答表示エリア --- */}
        {reply && (
          <div className="bg-white p-6 rounded-xl shadow-md border-2 border-orange-200 mb-8">
            <h2 className="text-xl font-bold mb-4 text-orange-700">🍳 提案レシピ</h2>
            <div className="whitespace-pre-wrap mb-6 leading-relaxed">
              {reply}
            </div>
            <button
              onClick={handleSave}
              className="w-full bg-green-600 text-white p-3 rounded-lg font-bold hover:bg-green-700 transition flex items-center justify-center gap-2"
            >
              <span>このレシピを保存する</span>
              <span className="text-xl">📝</span>
            </button>
            {/* ▼▼▼ (追加) Amazonアフィリエイト誘導ボタン ▼▼▼ */}
            <a
              href={`https://www.amazon.co.jp/s?k=${encodeURIComponent(input)}&tag=recipechef01-22`}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 block w-full bg-yellow-400 text-black p-3 rounded-lg font-bold text-center hover:bg-yellow-500 transition shadow-sm border-b-4 border-yellow-600 active:border-b-0 active:translate-y-1"
            >
              Amazonで「{input.length > 10 ? "食材" : input}」を探す 🛒
            </a>
            {/* ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ */}
          </div>
        )}

        {/* --- 保存したレシピ一覧エリア (デザイン変更) --- */}
        {savedRecipes.length > 0 && (
          <div className="mt-12">
            <h2 className="text-2xl font-bold mb-6 text-gray-700 border-b pb-2">
              📚 保存したレシピ帳 ({savedRecipes.length})
            </h2>
            <div className="space-y-6">
              {savedRecipes.map((recipe, index) => (
                <div key={index} className="bg-white rounded-lg shadow overflow-hidden border border-gray-200">
                  {/* タイトル部分 */}
                  <div className="bg-orange-100 p-4 border-b border-orange-200 flex justify-between items-center">
                    <div>
                      <h3 className="font-bold text-lg text-orange-800">{recipe.title}</h3>
                      <p className="text-xs text-gray-500">{recipe.date}</p>
                    </div>
                    <button
                      onClick={() => handleDelete(index)}
                      className="text-red-500 hover:text-white hover:bg-red-500 border border-red-500 px-3 py-1 rounded text-sm transition"
                    >
                      削除
                    </button>
                  </div>
                  
                  {/* 中身部分 */}
                  <div className="p-4 bg-white">
                    <p className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed">
                      {recipe.content}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}