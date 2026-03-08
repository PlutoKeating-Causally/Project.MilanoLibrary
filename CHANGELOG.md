# CHANGELOG

## 开发日志

### [V2.0.3] - 2026-03-08 - 知识交互功能完成

**Added:**
- KnowledgePoint 组件 (知识点交互卡片)
- 交互式标签页: 视频片段 / AI解释 / 思维导图
- AI 解释生成 API 集成
- 思维导图可视化组件
- 响应式 CSS 样式系统
- Git 工作流建立 (master/stage/production)

**改进:**
- VideoList 组件重构，支持知识点展示
- VideoUpload 用户体验优化
- 模态框关闭按钮
- 加载状态提示

**Git:**
- 初始化 Git 仓库
- 创建分支策略
- 提交 V2.0.2 和 V2.0.3

### [V2.0.2] - 2026-03-08 - MVP 核心流程完成

**Added:**
- FastAPI 后端主应用 (app/main.py)
- 视频上传 API (/api/v1/videos/upload)
- 视频状态查询 API (/api/v1/videos/{id}/status)
- 视频分析结果 API (/api/v1/videos/{id}/analysis)
- 模拟 AI 分析流程 (MVP 阶段)
- React 前端主应用
- VideoUpload 组件 (支持文件上传+自动触发分析)
- VideoList 组件 (视频列表展示+详情弹窗)
- 完整的 App.css 样式系统
- 后端 run.sh 一键启动脚本
- 前端 start.sh 一键启动脚本

**技术实现:**
- 后端: FastAPI + 内存存储 (MVP 阶段)
- 前端: React + CSS (无 Tailwind 依赖，减少构建复杂度)
- API 通信: Fetch API
- 状态管理: React useState

**可运行的最小闭环:**
1. 前端上传视频 → 2. 后端接收存储 → 3. 模拟 AI 分析 → 4. 前端展示结果

### [V2.0.1] - 2026-03-08 - 项目初始化完成

**Added:**
- 项目文件夹结构初始化 (backend/, frontend/, docs/)
- README.md 项目介绍文档
- docs/ARCHITECTURE.md 架构设计
- docs/API.md API 文档框架
- docs/QUICK_START.md 快速开始指南
- docs/plans/plan-01-init.md 开发计划
- .env.example 环境变量模板
- .gitignore Git 忽略规则

**技术决策:**
- 后端: Python FastAPI (异步高性能)
- 前端: React + TailwindCSS
- AI: Google Gemini API + Kimi API 双引擎
- 视频处理: FFmpeg

### [V2.0.0] - 2026-03-08 - 项目启动

**项目启动:**
- 项目启动，开始敏捷开发
- 确定产品愿景和核心功能

---

## 版本规范

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

### 版本号规则
- V2.x.x: 主版本 (重大功能更新)
- V2.0.x: 次版本 (新功能)
- V2.0.0: 修订版本 (Bug修复)

### 分类标签
- **Added**: 新功能
- **Changed**: 变更
- **Deprecated**: 即将移除
- **Removed**: 移除
- **Fixed**: Bug修复
- **Security**: 安全相关
