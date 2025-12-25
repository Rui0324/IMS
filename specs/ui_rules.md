# UI Rules (Element Plus)

> Based on patterns from the referenced Vue3 admin UI and generalized best practices for Element Plus dashboards.

## Layout
- Use a fixed sidebar + top header layout; content area scrolls with `main` padding `24px`.
- Card width on auth screens: 420–520px max; center horizontally/vertically with responsive padding on mobile (`min(5vw, 20px)`).
- Apply theme tokens via CSS variables (`--db-primary`, `--db-bg`, `--db-surface`, `--db-radius`) to enable light/dark extension.

## Typography & spacing
- Base font-size 14–15px; headings 18–20px for page titles.
- Form label width 110–120px; consistent `:label-position="'top'"` on narrow screens (<768px).
- Use `el-row`/`el-col` with `gutter="16"`; vertical rhythm `16/20/24px` for section spacing.

## Forms
- Wrap inputs in `el-form` with `status-icon` and `:rules` for required fields.
- Inputs align height (40–44px); use prefix icons (`User`, `Lock`, `Phone`, `Message`).
- Submit buttons `type="primary"` with loading state; secondary `text` or `default` for reset/cancel.
- Support Enter-to-submit on single forms (`@keyup.enter="onSubmit"`).
- Provide inline validation messages; avoid mixed inline styles—prefer scoped `<style lang="scss">`.

## Lists & tables
- Search bar above table; inline layout with `el-form` + `el-space`.
- Table uses `stripe` and `border` for clarity; sticky action column when width large.
- Pagination at bottom-right; props: `:page-size="query.pageSize"`, `:current-page="query.page"`, `layout="total, sizes, prev, pager, next, jumper"`.
- Use loading mask during fetch; empty state message customized to module context.

## Dialogs
- Dialog width 520–720px depending on form complexity; `destroy-on-close`.
- Footer buttons right-aligned; confirm button primary, cancel default.
- Support `before-close` to warn about unsaved changes when dirty.

## Notifications & feedback
- Success via `ElMessage.success`; errors via `ElMessage.error` with backend `msg`.
- Destructive operations require `ElMessageBox.confirm` with danger style.
- For long operations, use `ElNotification` with `duration: 0` and manual close.

## Uploads
- Use `el-upload` with `drag` style for documents/images; accept whitelist: `.pdf,.doc,.docx,.png,.jpg,.jpeg,.zip`.
- Set `:limit="3"` and show tip text about size (e.g., 10MB) and allowed types.
- On success, map server response `{ url }` to form model; show file list with name & size.

## Charts (ECharts)
- Place charts inside `el-card` with header actions (date picker, refresh).
- Responsive resize: register `resize` on window with debounced handler or `useResizeObserver`.
- Prefer color palette aligned with theme tokens; provide accessible legend labels.

## Routing & guards
- Routes include `meta.title`, `meta.icon`, `meta.roles`.
- Global before guard checks token; if missing redirect to `/login`; if role mismatch redirect to 403 page or first allowed route.
- Keep progress indicator (e.g., nprogress) optional; ensure async route import error fallback.

## Accessibility & responsiveness
- Minimum touch target 40px height; ensure focus outline visible.
- Breakpoints: stack form labels on <768px; collapse sidebar to icons-only; adjust card padding to 16px.
