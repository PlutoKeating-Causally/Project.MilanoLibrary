# Project.MilanoLibrary

## 项目简介

Project.MilanoLibrary 是一个视频内容智能提取与结构化学习平台，能够从复杂的长视频中提取结构化信息，并整理成逻辑清晰的完整讲义。

## 核心功能

- **视频内容提取**: 从视频中提取字幕、语音、画面信息
- **AI 结构化分析**: 使用 Gemini/Kimi 大模型分析内容结构
- **交互式学习**: 点击知识点查看视频片段、思维导图、AI解释
- **多模态报告**: 图文并茂的学习报告，支持书本/论文式排版

## 技术栈

- **前端**: React + TailwindCSS
- **后端**: Python FastAPI
- **AI**: Google Gemini API + Kimi API
- **视频处理**: FFmpeg
- **数据库**: SQLite (开发) / PostgreSQL (生产)

## 项目结构

```
Project.MilanoLibrary/
├── backend/          # Python FastAPI 后端
├── frontend/         # React 前端
├── docs/            # 文档
│   ├── plans/       # 开发计划
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── QUICK_START.md
├── README.md
├── CHANGELOG.md
└── .env
```

## 快速开始

### 方式一：本地开发

**后端:**
```bash
cd backend
./run.sh
```

**前端:**
```bash
cd frontend
./start.sh
```

### 方式二：Docker 部署

```bash
# 复制环境变量
cp .env.example .env
# 编辑 .env 填入 API Keys

# 启动所有服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端 API: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

详细说明见 [docs/QUICK_START.md](docs/QUICK_START.md)

## 架构设计

见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 开发日志

见 [CHANGELOG.md](CHANGELOG.md)

## 团队成员

- **Angela**: 前端 UI/UX 逻辑架构
- **Michel**: 后端业务流 + 快速部署 + 高并发处理

---
*Project of Causally Tech - 溯理科技*
