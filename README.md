# ARL MCP Improved v2.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0.0-green.svg)](https://github.com/modelcontextprotocol)

**专为AI安全分析设计的ARL MCP服务器，提供48个工具，覆盖漏洞扫描、敏感信息泄露检测、GitHub代码泄露监控等功能。**

改进版的 ARL (Asset Reconnaissance Lighthouse) MCP 服务器，支持通过环境变量配置，提供完整的 ARL API 集成。

## ✨ 核心特性

### 🔒 安全检测（19个工具）
- **Nuclei漏洞扫描** - 详细的漏洞信息和匹配内容
- **POC管理** - 漏洞验证脚本管理
- **敏感信息泄露检测** - 配置文件、备份文件、数据库泄露
- **GitHub代码泄露监控** - 监控GitHub上的敏感信息
- **Web指纹识别** - 自定义指纹规则
- **SSL证书查询** - 证书过期和安全检查

### 🤖 AI分析专用（3个工具）
- **漏洞汇总分析** - 一键获取所有漏洞统计
- **敏感信息泄露汇总** - 高风险泄露识别
- **GitHub泄露汇总** - 代码泄露风险评估

### 🚀 自动化功能
- **监控任务** - 定期自动扫描
- **策略管理** - 自定义扫描配置
- **数据导出** - CSV格式导出

### 🛠️ 基础功能
- 🔧 **灵活配置** - 支持环境变量配置 ARL URL 和 Token
- 🌍 **双语支持** - 自动检测并支持中英文响应
- 📊 **批量操作** - 支持批量任务管理和数据导出
- 🔍 **高级搜索** - 支持多条件过滤和精确查询
- 🚀 **易于集成** - 与 Kiro IDE 和其他 MCP 客户端无缝集成

## 📊 工具统计

- **总计：48个工具**
- 基础工具：3个
- 任务管理：8个
- 资产查询：12个
- 漏洞扫描：5个
- GitHub监控：4个
- 指纹识别：3个
- 策略管理：3个
- 监控任务：3个
- 数据导出：3个
- AI分析：3个
- **API覆盖率：45%**

## 🚀 快速开始

### AI安全评估（3步完成）

```python
# 1. 获取漏洞概况
vuln_summary = get_vulnerability_summary()

# 2. 获取敏感信息泄露概况
leak_summary = get_sensitive_leak_summary()

# 3. 获取GitHub代码泄露概况
github_summary = get_github_leak_summary()

# AI分析并生成报告
```

## 📦 安装

### 前置要求

- Python 3.10+
- ARL 服务器（运行中）
- ARL API Token

### 使用 uvx（推荐）

```bash
# 在 MCP 配置中添加
{
  "mcpServers": {
    "arl": {
      "command": "uvx",
      "args": ["--from", ".", "arl-mcp-improved"],
      "env": {
        "ARL_URL": "https://127.0.0.1:5192",
        "ARL_TOKEN": "your_token_here"
      }
    }
  }
}
```

### 使用 pip

```bash
# 克隆仓库
git clone <repository-url>
cd arl-mcp-improved

# 安装依赖
pip install -e .

# 设置环境变量
export ARL_URL="https://127.0.0.1:5192"
export ARL_TOKEN="your_token_here"

# 运行服务器
python server.py
```

## 🔧 配置

### 环境变量

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `ARL_URL` | ARL 服务器地址 | `https://127.0.0.1:5192` | 否 |
| `ARL_TOKEN` | ARL API Token | - | 是 |

### 获取 ARL Token

1. 登录 ARL Web 界面
2. 进入 "用户设置" 或 "API 设置"
3. 生成或复制 API Token
4. 将 Token 配置到环境变量中

## 📚 文档

### 快速导航
- 📖 [完整工具列表](./TOOLS.md) - 58个工具的详细说明
- 🔒 [安全检测工具](./SECURITY_TOOLS.md) - 19个安全相关工具
- 🤖 [AI使用指南](./AI_USAGE_GUIDE.md) - AI安全分析完整指南
- 📋 [缺失API分析](./MISSING_APIS.md) - 未来扩展计划
- ⚙️ [配置指南](./CONFIG_GUIDE.md) - 详细配置说明
- 🔄 [更新日志](./CHANGELOG.md) - 版本更新记录

## 💡 使用示例

### 创建扫描任务

```python
result = add_scan_task_and_prompt(
    name="测试扫描",
    target="example.com",
    domain_brute=True,
    port_scan=True,
    file_leak=True
)
```

### 查询漏洞

```python
# 查询所有严重漏洞
critical_vulns = search_nuclei_result_detail(
    severity="critical",
    size=100
)

# 获取漏洞汇总（AI分析专用）
summary = get_vulnerability_summary()
```

### 检测敏感信息泄露

```python
# 查询文件泄露
leaks = search_fileleak_detail(size=1000)

# 获取泄露汇总（AI分析专用）
leak_summary = get_sensitive_leak_summary()
```

### 监控GitHub代码泄露

```python
# 创建监控任务
create_github_monitor(
    name="example.com监控",
    keywords="example.com api_key password secret",
    cron="0 */6 * * *"
)

# 查询泄露结果
results = search_github_results(keyword="example.com")

# 获取泄露汇总（AI分析专用）
github_summary = get_github_leak_summary()
```

### 设置持续监控

```python
# 创建定期扫描任务
create_scheduler(
    name="每日安全扫描",
    target="example.com",
    cron="0 2 * * *"  # 每天凌晨2点
)
```

## 🎯 AI分析场景

### 场景1：全面安全评估
```python
# 一键获取完整安全状况
vuln_summary = get_vulnerability_summary()
leak_summary = get_sensitive_leak_summary()
github_summary = get_github_leak_summary()

# AI生成综合报告
```

### 场景2：漏洞深度分析
```python
# 查询高危漏洞
critical = search_nuclei_result_detail(severity="critical")
high = search_nuclei_result_detail(severity="high")

# AI分析并生成修复方案
```

### 场景3：敏感信息泄露调查
```python
# 查询所有泄露
leaks = search_fileleak_detail(size=1000)

# AI识别高风险泄露并生成应急响应计划
```

## 🔍 核心工具分类

### 任务管理（8个）
- `add_scan_task_and_prompt` - 创建扫描任务
- `add_scan_task_with_policy` - 使用策略创建任务
- `list_all_tasks` - 列出所有任务
- `query_task_status` - 查询任务状态
- `get_task_detail` - 获取任务详情
- `query_and_extract` - 提取任务结果
- `delete_task` - 删除任务
- `stop_task` - 停止任务
- `export_task_data` - 导出任务数据

### 资产查询（11个）
- `get_all_subdomains` - 获取子域名
- `query_ip_list` - 获取IP列表
- `query_site_list` - 获取站点列表
- `query_fileleak_list` - 获取文件泄露列表
- `search_asset_domain` - 搜索域名资产
- `search_asset_ip` - 搜索IP资产
- `search_site` - 搜索站点
- `search_cert` - 搜索SSL证书
- `search_url` - 搜索URL
- `search_fileleak_detail` - 搜索文件泄露详情

### 安全扫描（19个）
- `search_nuclei_result_detail` - Nuclei漏洞扫描
- `list_poc` - 列出POC
- `sync_poc` - 同步POC库
- `delete_poc` - 删除POC
- `create_github_monitor` - 创建GitHub监控
- `list_github_monitors` - 列出GitHub监控
- `search_github_results` - 搜索GitHub泄露
- `delete_github_monitor` - 删除GitHub监控
- `list_fingerprints` - 列出指纹
- `add_fingerprint` - 添加指纹
- `delete_fingerprint` - 删除指纹
- `get_vulnerability_summary` - 漏洞汇总（AI专用）
- `get_sensitive_leak_summary` - 泄露汇总（AI专用）
- `get_github_leak_summary` - GitHub泄露汇总（AI专用）

### 自动化（6个）
- `create_scheduler` - 创建监控任务
- `list_schedulers` - 列出监控任务
- `delete_scheduler` - 删除监控任务
- `create_policy` - 创建策略
- `list_policies` - 列出策略
- `delete_policy` - 删除策略

### 数据导出（3个）
- `export_domain_csv` - 导出域名
- `export_ip_csv` - 导出IP
- `export_site_csv` - 导出站点

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [ARL 项目](https://github.com/TophantTechnology/ARL)
- [MCP 协议](https://github.com/modelcontextprotocol)
- [FastMCP](https://github.com/jlowin/fastmcp)

## 📞 支持

如有问题，请：
1. 查看 [AI使用指南](./AI_USAGE_GUIDE.md)
2. 查看 [配置指南](./CONFIG_GUIDE.md)
3. 提交 Issue

---

**v2.0 更新亮点：**
- ✨ 新增33个工具（从25个增加到58个）
- 🔒 完整的安全检测功能
- 🤖 3个AI分析专用工具
- 📊 API覆盖率从22%提升到51%
- 📚 完整的AI使用指南
