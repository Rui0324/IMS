# Feature Matrix (No AI Scope)

> Scope excludes all AI-related features (no GPT/LangChain/Redis for AI, no AI recommend/QA). Stack assumptions: Django + DRF + JWT, MySQL, Vue3 + Element Plus + ECharts.

## P0 – Minimal Deployable (JWT + StudentInfo + Score + Basic Log)
- **Student authentication & profile**
  - Table: `users` (id, username, password_hash, role [student/teacher/admin], is_active, timestamps); `student_info` (user_id FK, full_name, major, grade, phone, email, updated_at).
  - Backend: ensure custom User model with role; serializers for auth and StudentInfo; views/urls for `/api/auth/login`, `/api/auth/refresh`, `/api/auth/me`, `/api/students/me` GET/PUT; permission classes enforcing role.
  - Frontend: login page/API wiring; Pinia auth store; route guard; Student profile page with editable form bound to `/api/students/me`.
  - Acceptance:
    1. POST `/api/auth/login` returns access/refresh for a student; using access to GET `/api/auth/me` shows role=student.
    2. Student visits “个人信息” page, edits phone/email, saves; reload shows updated values.
    3. Unauthenticated visit to any protected route redirects to `/login`.

- **Score entry & review basics**
  - Table: `scores` (id, project_id FK nullable, student_id FK, teacher_id FK, score_value, status [pending/approved/rejected], comment, created_at).
  - Backend: Score model/serializer/viewset; endpoints `/api/scores/` list/create/update with role checks (teacher create/update, student read own, admin full); status transitions constrained.
  - Frontend: Teacher “成绩录入” page with form + table; Student “成绩查看” page (read-only).
  - Acceptance:
    1. Teacher POST `/api/scores/` for student creates `pending` score.
    2. Teacher PATCH `/api/scores/{id}/` sets status=approved; student list shows updated status/value.
    3. Student attempting to PATCH a score receives 403.

- **Basic audit log middleware**
  - Table: `audit_logs` (id, user_id FK nullable, path, method, status_code, ip, duration_ms, summary, created_at).
  - Backend: middleware capturing requests/responses; serializer/view for `/api/admin/logs/` (admin only, paginated).
  - Frontend: Admin “审计日志” table page with filters (path, user, status).
  - Acceptance:
    1. After a student updates profile, an audit log entry exists with path `/api/students/me`, method PUT, status 200.
    2. Admin fetches `/api/admin/logs/?path=/api/students/me` and sees the entry.
    3. Non-admin hitting `/api/admin/logs/` receives 403.

## P1 – Core Platform Coverage (Projects, Messages, File Upload)
- **Project CRUD with attachments**
  - Table: `projects` (id, student_id FK, title, description, status [draft/submitted/approved/rejected], attachments JSON list, created_at, updated_at).
  - Backend: Model/serializer/viewset; endpoints `/api/projects/` CRUD with role rules (student owns create/update/delete before approval; teacher/admin read; admin can override status); upload endpoint `/api/projects/{id}/upload` validating whitelist `.pdf/.doc/.docx/.png/.jpg/.jpeg/.zip` and max size (10MB).
  - Frontend: Student “项目提交” page (form + upload), “项目列表/详情”; Teacher/Admin project review table with status chips and detail drawer.
  - Acceptance:
    1. Student creates project with title/description; list shows `draft`.
    2. Student uploads `report.pdf` to project; file list displays; backend stores URL.
    3. Teacher updates project status to approved via detail panel; student view reflects status.

- **Internal messaging**
  - Table: `messages` (id, sender_id FK, target_role nullable, target_user_id FK nullable, title, content, read_at nullable, created_at).
  - Backend: CRUD endpoints `/api/messages/`; permissions: sender must be authenticated; recipients fetch inbox (by role or direct user); read marking PATCH.
  - Frontend: Inbox page (list + pagination), message composer dialog (select role or specific user), detail view with mark-as-read.
  - Acceptance:
    1. Admin sends message to role=student; students see it in inbox list.
    2. Student opens message, detail shows content, `read_at` set.
    3. Teacher trying to delete a message they do not own receives 403.

## P2 – Admin Excellence (User/Role Mgmt, Permissions, Dashboard)
- **User & role/permission management**
  - Table adjustments: `users` add `is_active` toggle (if not present) and optional `notes`; optional `role` expansion to set choices; mapping for permissions table if granular (e.g., `role_permissions` with role name + perm key).
  - Backend: Admin endpoints `/api/admin/users/` for list/create/update/disable; `/api/admin/roles/` or constants for role-permission mapping; ensure JWT claims carry role; permission checks on all modules.
  - Frontend: Admin “用户管理” table with create/edit dialog (role select, activate/deactivate); “角色权限” page showing role-permission matrix (read-only or editable).
  - Acceptance:
    1. Admin creates teacher user; login works and `/api/auth/me` shows role=teacher.
    2. Admin disables a user; subsequent login attempt fails (401 or code indicating disabled).
    3. Student accessing admin route is redirected/blocked with 403.

- **Admin dashboard (ECharts)**
  - Data sources: `/api/admin/stats/` returning user counts by role, project totals by status, score approval rate, submissions over last 7 days.
  - Backend: Stats view aggregating counts; ensure queries indexed on status/created_at.
  - Frontend: ECharts dashboard with at least three charts (line for submissions trend, bar for projects by status, pie for users by role) and KPI cards.
  - Acceptance:
    1. Hitting `/api/admin/stats/` returns structured counts for roles, projects, scores.
    2. Dashboard renders charts without console errors; resizing window keeps charts responsive.
    3. Filters (e.g., date range) refresh charts via API call.
