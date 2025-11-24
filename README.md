# AI Recipe Chef 👨‍🍳 - 冷蔵庫の余り物を3つ星レシピへ

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![Gemini API](https://img.shields.io/badge/AI-Gemini_2.0_Flash-4285F4)

## 📖 概要 (Overview)
「冷蔵庫に半端な食材が残っている」「毎日の献立を考えるのが面倒」
そんな一人暮らしの学生や主婦の悩みを解決するために開発した、**食材入力型レシピ提案AIアプリ**です。

ユーザーが入力した食材と食べたいジャンルをもとに、生成AI（Google Gemini）が最適なレシピを考案。気に入ったレシピはタイトルをつけて保存し、自分だけのレシピ帳を作ることができます。

**[デモサイトはこちら](https://ai-recipe-chef.vercel.app/)**

## 🛠 使用技術 (Tech Stack)

### Frontend
- **Framework:** Next.js (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Persistence:** LocalStorage (MVPにおけるデータ永続化のため)

### Backend
- **Framework:** FastAPI (Python)
- **AI Model:** Google Gemini API (gemini-2.0-flash)
- **Client:** google-generativeai

## 💡 こだわったポイント (Key Highlights)

### 1. プロンプトエンジニアリングによる「人格」の実装
単にレシピを出力するだけでなく、システムプロンプトで「三ツ星レストランのシェフ」というペルソナを設定。
- ユーザーの入力を構造化して受け取る設計（食材 × ジャンル）
- 「美味しく作るためのワンポイントアドバイス」を必ず含めるよう指示し、UXを向上

### 2. ユーザー体験を意識した「保存機能」
AIの生成結果は一期一会であるため、気に入ったレシピをローカルストレージに保存できる機能を実装しました。
- ユーザー自身が識別しやすいよう、保存時に「タイトル」を付与できる仕様に変更
- ページ遷移やリロードをしてもデータが消失しない永続化処理

### 3. スケーラビリティを考慮した疎結合アーキテクチャ
将来的な機能拡張（ログイン機能、画像認識の実装など）を見据え、フロントエンド(Next.js)とバックエンド(FastAPI)を分離して開発。REST APIを通じてJSON形式でデータをやり取りするモダンな構成を採用しています。

## 🚀 機能一覧 (Features)
- **食材入力:** 自由記述で食材を入力
- **ジャンル選択:** 和食・洋食・中華・イタリアン・時短などから選択可能
- **レシピ生成:** AIによる高速なレシピ提案（材料・手順・コツ）
- **レシピ保存:** タイトルをつけてブラウザ内に保存
- **レシピ管理:** 保存したレシピの閲覧・削除

## 🏁 今後の展望 (Roadmap)
- [ ] **画像認識機能:** 食材の写真を撮るだけでAIが認識する機能（OpenCV/Gemini Vision）
- [ ] **ユーザー認証:** Supabase/Auth0を用いたログイン機能と、DBへのデータ移行
- [ ] **SNSシェア:** 生成されたレシピをX(Twitter)などでシェアする機能

## ⚠️ 現在の課題と今後の改善点 (Technical Debt & Roadmap)

このアプリはMVP（実用最小限の製品）として、**「3日間でのリリース」**を目標に開発しました。そのため、以下の点は意図的に簡易的な実装としていますが、今後改善予定です。

1.  **データの永続化:**
    * 現状: LocalStorageを使用（ブラウザ依存）。
    * 今後: **Supabase (PostgreSQL)** を導入し、クラウド保存とログイン機能を実装予定。
2.  **コードの保守性:**
    * 現状: `page.tsx` にロジックが集約されている。
    * 今後: UIパーツ（ボタン、リスト等）を別コンポーネントに切り出し、再利用性を高める。
3.  **エラーハンドリング:**
    * 現状: 基本的なtry-exceptのみ。
    * 今後: AIの生成失敗時の自動リトライ処理などを追加予定。
      
## 👨‍💻 Author
**aoma ikegaki**
- Web開発とデータサイエンスを学習中の学生エンジニアです。
- 「技術で日常の課題を解決する」をモットーに開発しています。
- GitHub:https://github.com/aoma8270-cyber
