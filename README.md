# 💬めんたいチャット
## DEMO

![output](https://github.com/user-attachments/assets/478f3db7-4f80-441d-82b5-ce2c3fbd430f)


## 🧑‍💻 Member
### Leader
- [oto](https://github.com/inooto/)
### SubLeader
- [masa](https://github.com/MasakiYoshida39)
### Frontend
- [masa](https://github.com/MasakiYoshida39)
- [futaba](https://github.com/futaba416)
### Backend
- [robe](https://github.com/jdelltty)
- [oto](https://github.com/inooto/)

## 🌱　Tech Stack
|Frontend|Backend|Infra|
|---|---|---|
|[![My Skills](https://skillicons.dev/icons?i=html,css,js)](https://skillicons.dev)|[![My Skills](https://skillicons.dev/icons?i=py,flask,mysql)](https://skillicons.dev)|[![My Skills](https://skillicons.dev/icons?i=docker)](https://skillicons.dev)|


# 🛠️ Setup
**最初に環境変数ファイル（.env）を作成します**
- Mac、Windows(PowerShell、Git Bash)の場合
```
cp .env.example .env
```
- Windows(コマンドプロンプト)の場合
```
copy .env.example .env
```

**起動方法**
1. イメージのビルド（初回のみ）
```.sh
docker compose build
```
2. コンテナの起動
```.sh
docker compose up
```

### ディレクトリ構成
```
.
├── ChatApp              # アプリディレクトリ
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── static          # 静的ファイル用ディレクトリ
│   ├── templates       # Template(HTML)用ディレクトリ
│   └── util
│       └── DB.py
├── Docker
│   ├── Flask
│   │   └── Dockerfile # Flask(Python)用Dockerファイル
│   └── MySQL
│       ├── Dockerfile  # MySQL用Dockerファイル
│       ├── init.sql    # MySQL初期設定ファイル
│       └── my.cnf
├── .env.example         # 環境変数ファイル（.env）を作成する為のサンプルファイル
├── docker-compose.yml   # Docker-composeファイル
└── requirements.txt     # 使用モジュール記述ファイル
```
