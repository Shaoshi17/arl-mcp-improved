# ARL MCP Improved

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0.0-green.svg)](https://github.com/modelcontextprotocol)

改进版的 ARL (Asset Reconnaissance Lighthouse) MCP 服务器，支持通过环境变量配置，提供完整的 ARL API 集成。

## ✨ 特性

- 🔧 **灵活配置** - 支持环境变量配置 ARL URL 和 Token
- 🌍 **双语支持** - 自动检测并支持中英文响应
- 🛠️ **完整功能** - 25+ 工具覆盖 ARL 主要功能
- 📊 **批量操作** - 支持批量任务管理和数据导出
- 🔍 **高级搜索** - 支持多条件过滤和精确查询
- 🚀 **易于集成** - 与 Kiro IDE 和其他 MCP 客户端无缝集成

## 功能特性

### 基础工具
- `extract_main_domain` - 从 HTTP 请求包中提取主域名
- `extract_domain_or_ip` - 提取域名、IP 或 IP 段
- `detect_reply_language` - 检测回复语言（中文/英文）

### 任务管理
- `add_scan_task_and_prompt` - 创建扫描任务
- `list_all_tasks` - 列出所有任务（支持分页和状态过滤）
- `query_task_status` - 查询任务状态
- `query_and_extract` - 提取任务完整结果
- `delete_task` - 删除任务（支持批量删除）
- `stop_task` - 停止正在运行的任务
- `export_task_data` - 导出任务的完整数据

### 资产查询
- `get_all_subdomains` - 获取所有子域名
- `query_ip_list` - 获取 IP 列表
- `query_site_list` - 获取站点列表
- `query_fileleak_list` - 获取文件泄露列表
- `search_asset_domain` - 搜索资产域名（支持高级过滤）
- `search_asset_ip` - 搜索资产 IP（支持端口信息）
- `search_site` - 搜索站点（支持标题、状态码过滤）

### 资产管理
- `list_asset_scopes` - 列出所有资产范围/分组
- `create_asset_scope` - 创建资产范围/分组

### 安全扫描
- `search_nuclei_result` - 搜索 Nuclei 漏洞扫描结果
- `list_policies` - 列出所有扫描策略

## 📦 安装

### 方式 1: 使用 pip（推荐）

```bash
pip install fastmcp requests tldextract urllib3
```

### 方式 2: 从源码安装

```bash
git clone https://github.com/yourusername/arl-mcp-improved.git
cd arl-mcp-improved
pip install -e .
```

### 依赖项

- Python >= 3.10
- fastmcp >= 0.2.0
- requests >= 2.31.0
- tldextract >= 5.0.0
- urllib3 >= 2.0.0

> **配置说明**: 安装后，需要在 MCP 客户端配置文件中设置 `ARL_URL` 和 `ARL_TOKEN` 环境变量（见下方配置章节）。

## ⚙️ 配置

### Kiro IDE 配置（推荐）

在 `.kiro/settings/mcp.json` 中添加，直接在配置中指定 URL 和 Token：

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
      "disabled": false,
      "autoApprove": [
        "list_all_tasks",
        "query_task_status",
        "search_asset_domain",
        "search_site",
        "query_fileleak_list"
      ]
    }
  }
}
```

### Claude Desktop 配置

在 `claude_desktop_config.json` 中添加：

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

### 环境变量方式（可选）

如果不想在配置文件中暴露 Token，也可以使用系统环境变量：

**Linux/Mac:**
```bash
export ARL_URL=https://your-arl-server:5003
export ARL_TOKEN=your-arl-token
```

**Windows:**
```cmd
set ARL_URL=https://your-arl-server:5003
set ARL_TOKEN=your-arl-token
```

或创建 `.env` 文件（参考 `.env.example`），但这种方式需要额外的环境变量加载工具。

> **注意**: 推荐直接在 MCP 配置文件的 `env` 字段中设置，这是最简单直接的方式。

## 使用示例

### 创建扫描任务
```python
add_scan_task_and_prompt(
    name="测试任务",
    target="example.com",
    domain_brute=True,
    port_scan=True,
    file_leak=True
)
```

### 查询任务列表
```python
list_all_tasks(page=1, size=10, status="done")
```

### 搜索资产
```python
# 搜索域名
search_asset_domain(domain="example.com", page=1, size=100)

# 搜索IP
search_asset_ip(ip="192.168", domain="example.com")

# 搜索站点
search_site(site="https://", title="登录", status=200)
```

### 查询漏洞
```python
search_nuclei_result(url="example.com", page=1, size=50)
```

### 管理资产范围
```python
# 创建资产范围
create_asset_scope(
    name="测试范围",
    scope="example.com\n192.168.1.0/24"
)

# 列出所有范围
list_asset_scopes(page=1, size=100)
```

## 与官方版本的区别

官方 `arl-mcp` 包的问题：
- 硬编码了 ARL URL (`https://127.0.0.1:5003`)
- 硬编码了 Token
- 无法通过配置文件修改

本改进版的优势：
- 支持通过环境变量配置 URL 和 Token
- 更完整的 API 覆盖（25+ 工具）
- 更好的错误处理和调试信息
- 支持批量操作
- 支持高级搜索和过滤

## 工具总数

当前版本提供 **25 个** MCP 工具，覆盖 ARL 的主要功能：
- 任务管理：7 个工具
- 资产查询：7 个工具
- 资产管理：2 个工具
- 安全扫描：2 个工具
- 辅助工具：3 个工具
- 数据导出：4 个工具

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关链接

- [ARL 官方项目](https://github.com/TophantTechnology/ARL)
- [Model Context Protocol](https://github.com/modelcontextprotocol)
- [FastMCP](https://github.com/jlowin/fastmcp)

## ⚠️ 免责声明

本工具仅用于授权的安全测试和资产管理。使用者应遵守相关法律法规，对使用本工具产生的后果负责。

## 💬 支持

如有问题或建议，请：
- 提交 [Issue](https://github.com/yourusername/arl-mcp-improved/issues)
- 查看 [工具文档](TOOLS.md)
- 参考 [示例配置](.env.example)
