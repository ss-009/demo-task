# デモ課題セットアップ手順

## 前提条件

- Docker / Docker Compose がインストールされていること
- curl が使えること（API 動作確認用）

---

## セットアップ手順

※以下の手順は、上から順にコマンドを実行することを想定しています

```bash
# ルートフォルダにて .env ファイル作成
cp env.example .env

# Docker起動
docker-compose up -d

# テーブル作成
docker-compose exec web python -m app.migrations.create_tables

# 動作確認
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"image_path": "/image/test.jpg"}'


# データベース確認
docker-compose exec db psql -U myuser -d db
SELECT * FROM ai_analysis_log;

# テスト実行
docker-compose exec web pytest -v

# Docker 停止
docker-compose down
```
