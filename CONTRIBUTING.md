# Contributing to ARL MCP Improved

感谢你考虑为 ARL MCP Improved 做出贡献！

## 如何贡献

### 报告 Bug

如果你发现了 bug，请创建一个 issue，包含以下信息：

1. Bug 的详细描述
2. 重现步骤
3. 预期行为
4. 实际行为
5. 环境信息（Python 版本、操作系统等）
6. 相关日志或错误信息

### 提出新功能

如果你有新功能的想法：

1. 先创建一个 issue 讨论这个功能
2. 说明为什么需要这个功能
3. 描述预期的行为
4. 如果可能，提供使用示例

### 提交代码

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

### 代码规范

- 遵循 PEP 8 Python 代码风格
- 添加适当的注释和文档字符串
- 确保代码可以通过现有的测试
- 如果添加新功能，请添加相应的测试

### 提交信息规范

使用清晰的提交信息：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建或辅助工具的变动

示例：
```
feat: 添加批量扫描任务功能
fix: 修复任务状态查询错误
docs: 更新 README 安装说明
```

## 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/yourusername/arl-mcp-improved.git
cd arl-mcp-improved
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -e .
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 ARL 配置
```

5. 运行测试
```bash
python server.py
```

## 问题和支持

如果你有任何问题，可以：

1. 查看 [README.md](README.md) 和 [TOOLS.md](TOOLS.md)
2. 搜索现有的 issues
3. 创建新的 issue

## 行为准则

- 尊重所有贡献者
- 保持友好和专业
- 接受建设性的批评
- 关注对项目最有利的事情

感谢你的贡献！🎉
