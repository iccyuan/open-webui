# Agent Browser 工具集成

本目录包含 Agent Browser 与 Open WebUI 集成所需的所有文件。

## 文件说明

### OpenAPI 方案（推荐）

- **openapi.json** - OpenAPI 3.0 规范文件
- **openapi-server.js** - Node.js API 服务器

### Python 工具方案（备选）

- **AgentBrowserTool.py** - Open WebUI Python 工具

## 快速开始

### 使用 OpenAPI 方案

1. 安装依赖：
```bash
cd mytools
npm install express cors swagger-ui-express
npm install -g agent-browser
```

2. 启动服务：
```bash
node openapi-server.js
```

3. 在 Open WebUI 中导入：
   - Workspace → Tools → Import Tool
   - 输入：`http://localhost:3000/openapi.json`

### 使用 Python 工具方案

1. 在 Open WebUI 中：
   - Workspace → Tools → Create Tool
   - 粘贴 `AgentBrowserTool.py` 内容

2. 启动 API 服务器（需要先运行 openapi-server.js）

## 更多信息

详细部署指南请查看项目根目录的 artifacts 文件夹中的 `walkthrough.md`。
