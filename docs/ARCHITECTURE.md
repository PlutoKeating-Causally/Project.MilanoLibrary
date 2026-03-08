# 架构设计文档 (ARCHITECTURE)

## 1. 系统概述

Project.MilanoLibrary 采用前后端分离架构，遵循高内聚低耦合原则。

## 2. 架构原则

### 2.1 高内聚低耦合
- 每个模块只负责单一职责
- 模块间通过标准接口通信
- 避免"牵一发而动全身"

### 2.2 敏捷迭代
- 先跑通最小可用核心流程
- 每次迭代一个独立功能
- 保留完整迭代记录

### 2.3 环境隔离
- 所有配置使用 .env 环境变量
- 禁止硬编码敏感信息
- 提供 .env.example 模板

## 3. 模块划分

### 3.1 后端模块 (backend/)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI 入口
│   ├── config.py         # 配置管理
│   ├── models/           # 数据模型
│   ├── routers/          # API 路由
│   ├── services/         # 业务逻辑
│   └── utils/            # 工具函数
├── requirements.txt
└── run.sh               # 一键运行脚本
```

**模块职责:**
- `models`: 数据库模型、Pydantic Schema
- `routers`: RESTful API 端点
- `services`: 核心业务逻辑（视频处理、AI调用）
- `utils`: 通用工具（文件处理、时间格式化等）

### 3.2 前端模块 (frontend/)

```
frontend/
├── src/
│   ├── components/       # 可复用组件
│   ├── pages/           # 页面组件
│   ├── services/        # API 调用
│   ├── hooks/           # React Hooks
│   └── utils/           # 工具函数
├── package.json
└── start.sh            # 一键运行脚本
```

## 4. 数据流

```
用户上传视频 → 后端接收 → FFmpeg提取信息 → AI分析结构化 → 存储 → 前端展示 → 交互式学习
```

## 5. 技术选型理由

### 5.1 FastAPI
- 异步高性能（Starlette + Pydantic）
- 自动 API 文档（OpenAPI/Swagger）
- 类型提示支持
- 适合高并发场景

### 5.2 React
- 组件化开发
- 生态系统成熟
- 适合交互式应用

### 5.3 AI 双引擎
- Google Gemini: 多模态理解、图像生成
- Kimi: 代码能力、中文优化

## 6. 部署架构

```
[Frontend] ←→ [Nginx] ←→ [FastAPI Backend] ←→ [Database]
                    ↓
              [AI Services]
           (Gemini + Kimi)
```

## 7. 扩展性考虑

- 模块化设计，方便替换组件
- 服务层抽象，便于切换 AI 提供商
- 数据库模型预留扩展字段

---
*架构设计: Angela & Michel*
*日期: 2026-03-08*
