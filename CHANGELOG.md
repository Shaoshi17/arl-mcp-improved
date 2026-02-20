# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-02-20

### Added
- 初始版本发布
- 支持环境变量配置 (ARL_URL, ARL_TOKEN)
- 完整的 ARL API 集成
- 任务管理功能
  - 添加扫描任务
  - 查询任务状态
  - 停止任务
  - 删除任务
  - 导出任务数据
- 资产搜索功能
  - 搜索域名资产
  - 搜索IP资产
  - 搜索站点
  - 查询文件泄露
- 资产范围管理
  - 列出资产范围
  - 创建资产范围
- 策略管理
  - 列出扫描策略
- 辅助工具
  - 域名/IP提取
  - 主域名提取
  - 语言检测
- 中英文双语支持
- 详细的工具文档 (TOOLS.md)

### Features
- 自动语言检测和响应
- 完整的错误处理
- SSL证书验证禁用（适用于自签名证书）
- 任务完成时间预估
- 详细的日志记录

### Documentation
- 完整的 README.md
- 工具使用文档 TOOLS.md
- 配置示例 .env.example
- API映射文档

## [Unreleased]

### Planned
- 支持更多 ARL 功能
- 添加批量操作支持
- 性能优化
- 更多的数据导出格式
