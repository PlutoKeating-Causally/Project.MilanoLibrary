# Git 工作流指南

## 分支策略

### 主要分支

| 分支 | 用途 | 保护级别 |
|------|------|----------|
| `production` | 生产环境代码 | 🔒 只读，禁止直接推送 |
| `stage` | 预发布/测试环境 | ⚠️ 需要 Code Review |
| `main` | 主开发分支 | 可推送 |

### 开发分支

每个开发者从 `main` 创建个人开发分支：
```bash
# Angela 的开发分支
git checkout -b angela/feature-name

# Michel 的开发分支  
git checkout -b michel/feature-name
```

## 工作流程

### 1. 开始新功能
```bash
# 从 main 拉取最新代码
git checkout main
git pull origin main

# 创建功能分支
git checkout -b feature/your-feature-name

# 开发并提交
git add .
git commit -m "feat: your feature description"
```

### 2. 合并到 Stage
```bash
# 切换到 stage
git checkout stage

# 拉取最新 stage
git pull origin stage

# 合并你的功能分支
git merge feature/your-feature-name

# 解决冲突（如果有）
# ...

# 推送到 stage
git push origin stage
```

### 3. 测试验证
- 在 stage 分支上进行完整测试
- 确保功能完整可用
- 确保没有破坏现有功能

### 4. 合并到 Production
```bash
# 切换到 production
git checkout production

# 拉取最新
git pull origin production

# 合并 stage
git merge stage

# 推送到 production
git push origin production
```

## 冲突处理

### 原则
1. **沟通优先** - 发生冲突时，双方沟通解决方案
2. **单人决策** - 指定一人负责编辑冲突文件
3. **共同认可** - 解决方案需双方认可
4. **测试验证** - 解决后必须测试验证

### 处理流程
```bash
# 1. 发现冲突时停止
git status  # 查看冲突文件

# 2. 沟通确定解决方案
# (与队友讨论)

# 3. 指定一人编辑冲突文件
# 编辑文件，保留双方需要的代码

# 4. 标记冲突已解决
git add <conflict-file>

# 5. 完成合并
git commit -m "merge: resolve conflicts between X and Y"

# 6. 测试验证
# 运行测试确保功能正常
```

## 提交规范

### 提交信息格式
```
类型: 简短描述

详细说明（可选）
```

### 类型标签
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 示例
```bash
git commit -m "feat: add video upload API endpoint"
git commit -m "fix: resolve CORS issue in production"
git commit -m "docs: update API documentation"
```

## 最佳实践

### ✅ 应该做的
- 经常提交小的、完整的更改
- 写清晰的提交信息
- 推送前先在本地测试
- 及时拉取远程更新
- 功能完成后立即合并

### ❌ 不应该做的
- 长时间不提交
- 提交不完整的代码
- 直接在 production 分支开发
- 不测试就推送
- 忽视冲突警告

---
*Git 工作流指南 - Project.MilanoLibrary*
