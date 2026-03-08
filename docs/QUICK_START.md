# 快速开始

## 环境要求

- Python 3.9+
- Node.js 18+
- FFmpeg

## 1. 克隆项目

```bash
git clone <repository_url>
cd Project.MilanoLibrary
```

## 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的 API Keys
```

## 3. 启动后端

```bash
cd backend
pip install -r requirements.txt
./run.sh
```

后端将在 `http://localhost:8000` 启动

## 4. 启动前端

```bash
cd frontend
npm install
./start.sh
```

前端将在 `http://localhost:3000` 启动

## 5. 访问应用

打开浏览器访问: `http://localhost:3000`

## 开发模式

### 后端开发
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### 前端开发
```bash
cd frontend
npm run dev
```

## 常见问题

### Q: FFmpeg 未安装
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Q: API Key 错误
确保 `.env` 文件正确配置：
```
GOOGLE_API_KEY=your_google_key
KIMI_API_KEY=your_kimi_key
```

---
*文档: Michel*
*日期: 2026-03-08*
