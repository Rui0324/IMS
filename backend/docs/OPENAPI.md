# API 文档说明

项目默认使用 DRF 自动生成的 OpenAPI Schema，可通过 `python manage.py generateschema --format openapi` 生成。
推荐在本地安装 `drf-spectacular` 或使用 `drf-yasg` 进一步美化，本示例保持轻量。

关键端点：
- `/api/auth/login` 登录获取 JWT
- `/api/projects/` 项目 CRUD
- `/api/ai/recommend` AI 推荐
