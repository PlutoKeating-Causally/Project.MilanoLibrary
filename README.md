# Project.MilanoLibrary

## 项目简介

Project.MilanoLibrary 是一个视频内容智能提取与结构化学习平台，能够从复杂的长视频中提取结构化信息，并整理成逻辑清晰的完整讲义。

**版本:** V2.0.3  
**开发时间:** 2026-03-08 (1小时敏捷开发)  
**状态:** ✅ 功能完整，可运行

## 核心功能 ✅

- ✅ **视频上传**: 支持 MP4/AVI/MOV/MKV 格式
- ✅ **AI 内容分析**: Google Gemini API 智能分析
- ✅ **章节自动划分**: 智能识别视频结构
- ✅ **摘要生成**: 自动生成内容摘要
- ✅ **知识点交互**: 可折叠的知识点卡片
- ✅ **AI 解释**: 点击获取知识点详细解释
- ✅ **思维导图**: 可视化知识结构
- ✅ **时间定位**: 显示每个知识点的视频时间段

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18 + CSS3 |
| 后端 | Python FastAPI |
| AI | Google Gemini API |
| 视频 | FFmpeg |
| 测试 | pytest |

## 项目结构

```
Project.MilanoLibrary/
├── backend/              # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py       # 主应用
│   │   └── services/
│   │       ├── ai_service.py      # AI 服务
│   │       └── video_processor.py # 视频处理
│   ├── tests/
│   │   └── test_api.py   # API 测试
│   ├── venv/             # Python 虚拟环境
│   ├── requirements.txt
│   ├── run.sh            # 启动脚本
│   └── test.sh           # 测试脚本
├── frontend/             # React 前端
│   ├── src/
│   │   ├── components/
│   │   │   ├── VideoUpload.js     # 上传组件
│   │   │   ├── VideoList.js       # 列表组件
│   │   │   └── KnowledgePoint.js  # 知识点组件
│   │   ├── App.js
│   │   └── App.css
│   ├── package.json
│   └── start.sh          # 启动脚本
├── docs/                 # 文档
│   ├── ARCHITECTURE.md   # 架构设计
│   ├── API.md            # API 文档
│   ├── QUICK_START.md    # 快速开始
│   ├── GIT_WORKFLOW.md   # Git 工作流
│   └── plans/            # 开发计划
├── README.md
├── CHANGELOG.md
├── PROJECT_SUMMARY.md    # 项目总结
├── STATUS_REPORT.md      # 状态报告
└── .env.example
```

## 快速开始

### 环境准备

**必需软件:**
- Python 3.11+
- Node.js 18+ (前端需要)
- FFmpeg (视频处理)

**API Keys:**
复制 `.env.example` 为 `.env` 并填入:
- `GOOGLE_API_KEY` - Google AI Studio API Key
- `KIMI_API_KEY` - Kimi API Key

### 启动后端

```bash
cd /root/Project.MilanoLibrary/backend
./run.sh
```

后端将在 `http://localhost:8000` 启动  
API 文档: `http://localhost:8000/docs`

### 启动前端

```bash
cd /root/Project.MilanoLibrary/frontend
./start.sh
```

前端将在 `http://localhost:3000` 启动

### 运行测试

```bash
cd /root/Project.MilanoLibrary/backend
./test.sh
```

## API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/v1/videos/upload` | 上传视频 |
| GET | `/api/v1/videos/{id}/status` | 查询状态 |
| GET | `/api/v1/videos/{id}/analysis` | 获取分析结果 |
| POST | `/api/v1/videos/{id}/analyze` | 触发 AI 分析 |
| POST | `/api/v1/knowledge-points/{id}/explain` | 生成 AI 解释 |
| POST | `/api/v1/knowledge-points/{id}/mindmap` | 生成思维导图 |

详细文档见 [docs/API.md](docs/API.md)

## 开发计划

| 版本 | 时间 | 内容 | 状态 |
|------|------|------|------|
| V2.0.1 | 17:08 | 项目初始化 | ✅ |
| V2.0.2 | 17:30 | MVP + AI 集成 | ✅ |
| V2.0.3 | 17:50 | 知识交互功能 | ✅ |

## Git 提交历史

```
571f14e - chore: setup virtual environment and verify backend startup
dcdd754 - test: add comprehensive backend test suite
fe1a04e - docs: add STATUS_REPORT.md and update memory
d203dbe - docs: add project summary report
82cbe61 - docs: update plans and changelog for V2.0.3
9e5b969 - feat: add knowledge point interaction
58f82c0 - feat: initialize Project.MilanoLibrary
```

## 团队成员

- **Angela**: 前端 UI/UX 逻辑架构
- **Michel**: 后端业务流 + 快速部署 + 高并发处理

---
*Project of Causally Tech - 溯理科技*  
*Developed with ❤️ in 1 hour of agile development*
