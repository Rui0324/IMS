# 深蓝双创信息管理系统（开发导向版）

面向校园创新创业的全栈示例，包含 Django + Vue3 双端、AI Mock 接口、Docker Compose 支持。

## 快速开始（本地）
1. 安装 Python 3.12+、Node 18+、MySQL、Redis，建议 WSL2 环境。
2. 进入 `backend/`，复制 `.env.example` 为 `.env` 并调整数据库/Redis 配置。
3. 创建虚拟环境并安装依赖：`pip install -r requirements.txt`。
4. 初始化数据库：`python manage.py migrate`，如需管理员：`python manage.py createsuperuser`。
5. 启动后端：`python manage.py runserver 0.0.0.0:8000`。
6. 前端：进入 `frontend/`，复制 `.env.example` 为 `.env`，执行 `npm install`，`npm run dev`。

## Docker Compose
1. 复制 `backend/.env.example` 为 `backend/.env`。
2. 运行 `docker compose up --build`，默认服务包括 MySQL、Redis、backend。
3. 后端监听 8000 端口，前端可本地 `npm run dev` 连接。

## AI 配置
- 若提供 `OPENAI_API_KEY`，将尝试真实 RAG；缺省时返回 mock 文本，接口协议保持一致。
- 本地知识库存放 `data/knowledge/*.txt`。

## 目录
- backend：Django API、pytest、lint 配置。
- frontend：Vite + Vue3 管理端。
- data/knowledge：RAG 文本库。

## 关键接口
- 认证：`/api/auth/login`, `/api/auth/refresh`, `/api/auth/me`, `/api/auth/register`
- 学生信息：`/api/students/me` (GET/PUT)
- 项目：`/api/projects/` CRUD，`/api/projects/{id}/upload`
- 评分审核：`/api/scores/`
- 站内信：`/api/messages/`
- 管理：`/api/admin/users/`, `/api/admin/logs/`, `/api/admin/stats/`
- AI：`/api/ai/recommend`, `/api/ai/qa`

## 初始化账号
- 管理员可通过 `createsuperuser` 或 `/api/auth/register` 创建；可在 `docker compose up` 后进入容器执行管理命令。
