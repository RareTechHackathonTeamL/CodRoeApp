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
|![Static Badge](https://camo.githubusercontent.com/c4b74b64559a8adc26ef76c3dc0115421391cba4e9485cdc37d6c9feb1165318/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f48544d4c2d4533344632363f6c6f676f3d68746d6c35266c6f676f436f6c6f723d7768697465)<br>![Static Badge](https://camo.githubusercontent.com/8aa65fad6506c97ce05bf0410fe83fcdccee372f0f209bfc260fa35757e7e7ef/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4353532d3135373242363f6c6f676f3d63737333266c6f676f436f6c6f723d7768697465)<br>![Static Badge](https://camo.githubusercontent.com/6453965f3f4c526584dfdcd07b54605ebf2f501b5c6c46cbd6baba7ed02e80ef/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4a6176615363726970742d4637444631453f6c6f676f3d6a617661736372697074266c6f676f436f6c6f723d626c61636b)|![Static Badge](https://camo.githubusercontent.com/8631004f94179b636f7cfec68f970c37927c95757a26fa656c58bc67015bc9f0/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d3337373641423f6c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465)<br>![Static Badge](https://camo.githubusercontent.com/e0a9d967cb517dcdad2c0809c2f451a40b478cdd5119d6998b036f14a05ec24b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f466c61736b2d3030303030303f6c6f676f3d666c61736b266c6f676f436f6c6f723d7768697465)<br>![Static Badge](https://camo.githubusercontent.com/035ddd55035902181a1a4586ae4a8861fd1dd34b18fb8f3ad6caea02d4259e9c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4d7953514c2d3434373941313f6c6f676f3d6d7973716c266c6f676f436f6c6f723d7768697465)|![Static Badge](https://camo.githubusercontent.com/0bba72db052794db7b917abda181702a7af7d352e704868f8b0eef45304d7dcf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f636b65722d3234393645443f6c6f676f3d646f636b6572266c6f676f436f6c6f723d7768697465)|


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
