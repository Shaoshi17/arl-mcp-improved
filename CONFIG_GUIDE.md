# 配置指南

## 环境变量配置方式

ARL MCP Improved 通过环境变量读取配置。有以下几种方式设置环境变量：

### ✅ 方式 1: MCP 配置文件（推荐）

这是最简单直接的方式，直接在 MCP 客户端配置文件中设置。

#### Kiro IDE

编辑 `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "arl": {
      "command": "python3",
      "args": ["/path/to/arl-mcp-improved/server.py"],
      "env": {
        "ARL_URL": "https://your-arl-server:5003",
        "ARL_TOKEN": "your-arl-token"
      },
      "disabled": false
    }
  }
}
```

#### Claude Desktop

编辑 `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arl": {
      "command": "python3",
      "args": ["/path/to/arl-mcp-improved/server.py"],
      "env": {
        "ARL_URL": "https://your-arl-server:5003",
        "ARL_TOKEN": "your-arl-token"
      }
    }
  }
}
```

**优点:**
- ✅ 简单直接，一次配置永久生效
- ✅ 不需要额外的环境变量设置
- ✅ 配置集中管理
- ✅ 支持多个 MCP 服务器不同配置

**缺点:**
- ⚠️ Token 明文存储在配置文件中

---

### 方式 2: 系统环境变量

如果不想在配置文件中暴露 Token，可以使用系统环境变量。

#### Linux/Mac

**临时设置（当前终端会话）:**
```bash
export ARL_URL=https://your-arl-server:5003
export ARL_TOKEN=your-arl-token
```

**永久设置（添加到 shell 配置文件）:**

Bash (~/.bashrc 或 ~/.bash_profile):
```bash
echo 'export ARL_URL=https://your-arl-server:5003' >> ~/.bashrc
echo 'export ARL_TOKEN=your-arl-token' >> ~/.bashrc
source ~/.bashrc
```

Zsh (~/.zshrc):
```bash
echo 'export ARL_URL=https://your-arl-server:5003' >> ~/.zshrc
echo 'export ARL_TOKEN=your-arl-token' >> ~/.zshrc
source ~/.zshrc
```

#### Windows

**临时设置（当前命令行会话）:**
```cmd
set ARL_URL=https://your-arl-server:5003
set ARL_TOKEN=your-arl-token
```

**永久设置（系统环境变量）:**
```powershell
# PowerShell (管理员权限)
[System.Environment]::SetEnvironmentVariable('ARL_URL', 'https://your-arl-server:5003', 'User')
[System.Environment]::SetEnvironmentVariable('ARL_TOKEN', 'your-arl-token', 'User')
```

或通过图形界面：
1. 右键"此电脑" -> "属性"
2. "高级系统设置" -> "环境变量"
3. 在"用户变量"中添加 `ARL_URL` 和 `ARL_TOKEN`

**MCP 配置（不设置 env）:**
```json
{
  "mcpServers": {
    "arl": {
      "command": "python3",
      "args": ["/path/to/arl-mcp-improved/server.py"]
    }
  }
}
```

**优点:**
- ✅ Token 不在配置文件中
- ✅ 可以在多个应用间共享配置

**缺点:**
- ⚠️ 设置较复杂
- ⚠️ 需要重启应用才能生效
- ⚠️ 不同 MCP 服务器无法使用不同配置

---

### 方式 3: .env 文件（不推荐）

这种方式需要额外的工具来加载 .env 文件，通常不推荐。

1. 复制 `.env.example` 为 `.env`:
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件:
```bash
ARL_URL=https://your-arl-server:5003
ARL_TOKEN=your-arl-token
```

3. 使用 python-dotenv 加载（需要修改 server.py）:
```python
from dotenv import load_dotenv
load_dotenv()
```

**优点:**
- ✅ Token 不在配置文件中
- ✅ 便于版本控制（.env 在 .gitignore 中）

**缺点:**
- ⚠️ 需要额外依赖 python-dotenv
- ⚠️ 需要修改代码
- ⚠️ 不是标准 MCP 配置方式

---

## 推荐配置方案

### 个人使用
**推荐: 方式 1（MCP 配置文件）**
- 简单直接，无需额外设置
- 适合个人开发环境

### 团队使用
**推荐: 方式 2（系统环境变量）**
- Token 不在配置文件中，更安全
- 可以统一管理凭证

### 生产环境
**推荐: 方式 2（系统环境变量）+ 密钥管理**
- 使用密钥管理服务（如 AWS Secrets Manager、HashiCorp Vault）
- 通过脚本动态设置环境变量

---

## 配置验证

### 检查环境变量是否设置

**Linux/Mac:**
```bash
echo $ARL_URL
echo $ARL_TOKEN
```

**Windows:**
```cmd
echo %ARL_URL%
echo %ARL_TOKEN%
```

### 测试 MCP 服务器

直接运行 server.py 测试:
```bash
python3 server.py
```

如果配置正确，应该看到 MCP 服务器启动信息。

---

## 常见问题

### Q: 为什么有 .env.example 文件？
A: 仅作为参考。通常情况下，你应该在 MCP 配置文件的 `env` 字段中设置环境变量，而不是使用 .env 文件。

### Q: 可以同时使用多种方式吗？
A: 可以，但优先级是：MCP 配置 env > 系统环境变量 > .env 文件

### Q: 如何在不同环境使用不同配置？
A: 使用 MCP 配置文件的 `env` 字段，可以为不同的 MCP 服务器实例设置不同的配置。

### Q: Token 安全吗？
A: 
- MCP 配置文件: Token 明文存储，适合个人开发环境
- 系统环境变量: 相对安全，但仍可被有权限的用户查看
- 生产环境: 建议使用密钥管理服务

---

## 配置示例

### 示例 1: 本地开发（Kiro IDE）

```json
{
  "mcpServers": {
    "arl-local": {
      "command": "python3",
      "args": ["D:/projects/arl-mcp-improved/server.py"],
      "env": {
        "ARL_URL": "https://localhost:5003",
        "ARL_TOKEN": "local-dev-token"
      }
    }
  }
}
```

### 示例 2: 多环境配置

```json
{
  "mcpServers": {
    "arl-dev": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": {
        "ARL_URL": "https://dev-arl.company.com:5003",
        "ARL_TOKEN": "dev-token"
      }
    },
    "arl-prod": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": {
        "ARL_URL": "https://prod-arl.company.com:5003",
        "ARL_TOKEN": "prod-token"
      }
    }
  }
}
```

### 示例 3: 使用系统环境变量

```json
{
  "mcpServers": {
    "arl": {
      "command": "python3",
      "args": ["/path/to/server.py"]
      // 不设置 env，使用系统环境变量
    }
  }
}
```

---

**最后更新**: 2024-02-20
