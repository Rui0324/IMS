# Reference Project Notes

> Source intent: SeasonL student management system (Spring Boot backend) and student-mangement-system-web (Vue3 + Element Plus admin UI). Remote clone was attempted but blocked by network proxy (HTTP 403). The patterns below consolidate publicly documented conventions and commonly observed structures in these repositories to guide DeepBlue IMS alignment.

## Frontend (Vue3 + Vite + Element Plus)

- **Layout & navigation**
  - Left sidebar + top breadcrumb/header; routes grouped by role (admin/teacher/student) with meta roles for guards.
  - Menu items carry `icon`, `title`, and `path`; children for nested sections (e.g., student info, course/project, score review).
  - Dynamic routes often loaded via `modules` under `router` using lazy imports for pages.
- **Pages**
  - **List pages**: search form (inline) above a `el-table` with pagination; actions column for edit/delete/detail; uses `v-loading` on table; date range filter for time-based queries.
  - **Form pages**: `el-form` with label width 100–120px, `:rules` for required fields; dialog-based create/edit; reset & submit buttons.
  - **Dashboard/Statistics**: cards for summary counters (users/projects/tasks), `ECharts` line/bar/pie combos; uses responsive grid (`el-row`/`el-col`) with `gutter`.
  - **Auth**: login page uses centered card, remembers token in localStorage; route guard checks token + role before entering protected routes.
- **State & data**
  - Axios instance with baseURL + token header; response interceptor handles unified `{code, msg, data}` contract; auto-redirect to login on 401.
  - Pinia store for user info & token; refresh user profile on page reload; role-based menu generation.
- **UX patterns**
  - Buttons use `type="primary"` for submit, `text` for secondary; confirmation dialogs for destructive actions.
  - Upload controls for attachments (pdf/doc/docx/png/jpg/zip) with size/type validation and `el-upload` drag card style.

## Backend (Spring Boot reference)

- **Module split**
  - Core domains: student, teacher, course/project, score/review, notice/message; separate controller/service/mapper layers.
  - Security module with JWT filter, login endpoint, role-based access using annotations.
  - Audit logging via AOP or interceptor capturing user, URI, method, status, and execution time.
- **API behavior**
  - Unified response wrapper `{ code: 0, msg: "success", data: {...} }`; errors use non-zero code with message.
  - Pagination via `pageNum`, `pageSize` query params; return `total`, `list`, `pageNum`, `pageSize`.
  - Controllers validate ownership/role (student vs teacher vs admin) before CRUD.
  - File upload endpoint with whitelist & max size; stored under configurable `upload` path.
- **Utilities**
  - Global exception handler for validation/auth errors; `@ControllerAdvice`.
  - MyBatis/Mapper layer with XML or annotation queries; service layer handles business rules and audit insertions.

## Reusable ideas for DeepBlue IMS

- Keep unified Axios/DRF client handling: token header, code-based error branch, 401 redirect.
- Maintain menu schema with meta `role` for guard and breadcrumbs; generate dynamic sidebar from route tree.
- Adopt dashboard layout with metric cards + mixed ECharts (line/bar/pie) fed by `/api/admin/stats`.
- Standardize upload validation (suffix + max size) consistent across UI and backend configs.
- Continue audit logging: capture user, IP, path, method, status, duration; expose filterable admin log list.
