# API Contract Guidelines

> Harmonized from common patterns in the referenced Spring Boot/ Vue admin stack and aligned to DeepBlue IMS (Django + DRF).

## Response envelope
- Standard shape:  
  ```json
  { "code": 0, "msg": "success", "data": { ... } }
  ```
- Non-zero `code` indicates error; `msg` carries human-readable reason; `data` may be `null` on failure.
- HTTP status:
  - 200 for successful business responses (even with empty lists).
  - 400 for validation errors; 401 for auth; 403 for permission; 404 for missing resources; 500 for server errors.

## Pagination
- Request query params:
  - `page` (default 1)
  - `pageSize` (default 10/20)
  - Filters are snake_case (e.g., `status`, `keyword`, `startDate`, `endDate`, `role`).
- Response payload:
  ```json
  {
    "code": 0,
    "msg": "success",
    "data": {
      "list": [ ... ],
      "total": 123,
      "page": 1,
      "pageSize": 20
    }
  }
  ```

## JWT & auth
- Login returns tokens:
  ```json
  { "code": 0, "msg": "success", "data": { "access": "<jwt>", "refresh": "<jwt>", "user": { "id": 1, "username": "alice", "role": "student" } } }
  ```
- Headers: `Authorization: Bearer <access>`.
- Refresh endpoint returns new `access`; keep `refresh` stable until expiry/rotation.
- Role claims drive frontend route guards via `meta.roles`.

## Errors & codes
- Suggested codes: `0` success; `1001` validation error; `1002` auth failed; `1003` permission denied; `1004` not found; `200x` business-specific errors (e.g., `2001` duplicate name, `2002` upload type invalid).
- Error response example:
  ```json
  { "code": 1002, "msg": "Invalid username or password", "data": null }
  ```
- Validation errors may include field map:
  ```json
  { "code": 1001, "msg": "Validation failed", "data": { "field": ["required"] } }
  ```

## Query parameter naming
- Time ranges: `startDate`, `endDate`; prefer ISO strings.
- Sorting: `sortField`, `sortOrder` (`asc`/`desc`).
- Filters: `status`, `role`, `keyword`, `category`, `ownerId`.

## Upload API
- Request: multipart/form-data field `file`; optional `description`.
- Constraints: suffix whitelist `.pdf,.doc,.docx,.png,.jpg,.jpeg,.zip`; size up to 10MB.
- Response: `{ "code": 0, "msg": "success", "data": { "id": 10, "name": "file.pdf", "url": "/media/..." } }`.

## Audit & logging
- On sensitive operations, backend records user, role, IP, path, method, status, duration, and brief summary.
- Admin log list endpoint should accept filters: `user`, `path`, `status`, `method`, `startDate`, `endDate`, with paginated response.
