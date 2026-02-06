# Railway 部署指南

## 快速部署

### 方法1：一键部署（推荐）

点击下方按钮直接部署到 Railway：

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Thelia-Lzr/Thelia-mcp)

### 方法2：从 GitHub 仓库部署

1. 访问 [Railway](https://railway.app/)
2. 使用 GitHub 账号登录
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 授权 Railway 访问你的 GitHub 账号
6. 选择 `Thelia-Lzr/Thelia-mcp` 仓库
7. Railway 会自动检测配置并开始部署

### 方法3：使用 Railway CLI

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 部署
railway up
```

## 部署后配置

### 获取服务 URL

部署完成后，Railway 会自动生成一个公开的 URL，格式类似：
```
https://your-app-name.up.railway.app
```

你可以在 Railway 项目面板的 "Settings" -> "Domains" 中查看和配置域名。

### 测试部署

部署成功后，访问以下 URL 测试服务：

```bash
# 查看服务信息
curl https://your-app-name.up.railway.app/

# 查看 API 文档
访问: https://your-app-name.up.railway.app/docs

# 测试 API
curl https://your-app-name.up.railway.app/api/age
```

## 配置说明

项目包含以下 Railway 配置文件：

### Procfile
```
web: python http_server.py
```
指定启动命令为运行 HTTP 服务器。

### railway.toml
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python http_server.py"
healthcheckPath = "/"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
```

配置说明：
- **builder**: 使用 Nixpacks 自动检测和构建
- **startCommand**: 服务启动命令
- **healthcheckPath**: 健康检查端点
- **healthcheckTimeout**: 健康检查超时时间（秒）
- **restartPolicyType**: 失败时自动重启
- **restartPolicyMaxRetries**: 最多重试 10 次

### runtime.txt
```
python-3.11
```
指定使用 Python 3.11 运行时。

## 环境变量

Railway 会自动设置 `PORT` 环境变量，服务会自动使用该端口。无需手动配置。

## 注意事项

1. **免费额度**: Railway 提供免费额度，超出部分需要付费
2. **自动休眠**: 免费计划可能会在无流量时自动休眠服务
3. **MCP 模式**: Railway 部署的是 HTTP REST API 模式，不支持 MCP stdio 模式
4. **CORS**: 已配置 CORS 支持跨域访问，适合前端应用调用

## 故障排除

### 部署失败

如果部署失败，检查 Railway 的构建日志：
1. 进入项目面板
2. 点击 "Deployments"
3. 查看失败的部署日志

常见问题：
- **依赖安装失败**: 检查 `requirements.txt` 是否正确
- **端口冲突**: 确保代码使用 `PORT` 环境变量
- **内存不足**: 免费计划有内存限制，考虑升级

### 服务无响应

1. 检查服务是否正在运行
2. 查看 Runtime logs
3. 确认健康检查端点 `/` 返回正常

## 其他云平台

本服务也可以部署到其他平台：

- **Heroku**: 使用相同的 Procfile
- **Render**: 自动检测 Python 项目
- **Fly.io**: 需要创建 fly.toml
- **Vercel**: 需要配置 serverless 函数

## 更多信息

- [Railway 官方文档](https://docs.railway.app/)
- [Railway Python 部署指南](https://docs.railway.app/guides/python)
