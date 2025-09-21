created: 2025-09-21 22:55:51
modified: 2025-09-21 22:55:51
aliases: [2025-09-21]
tags: [daily, 2025-09-21]

---
# 📄 System Requirement Document (SRD)

## Module: Notes Management

---

## 1. Giới thiệu

### 1.1 Mục tiêu

Module **Notes Management** cho phép người dùng tạo, quản lý và chia sẻ ghi chú (notes) trong hệ thống web hiện tại. Tính năng hướng tới:

- Hỗ trợ ghi chú nhanh, trực quan, nhiều định dạng.
    
- Quản lý có cấu trúc (tags, folders, projects).
    
- Hỗ trợ cộng tác và nhắc nhở.
    
- Dễ dàng tích hợp vào web/app sẵn có.
    

### 1.2 Phạm vi

- Tích hợp trực tiếp vào hệ thống web hiện tại.
    
- Sử dụng hệ thống **authentication & user management** đã có sẵn.
    
- Module có thể được mở rộng thành microservice độc lập trong tương lai.
    

---

## 2. Tính năng

### 2.1 CRUD cơ bản

- Tạo mới note.
    
- Chỉnh sửa nội dung note.
    
- Xoá note (move to trash).
    
- Xem chi tiết note.
    
- Khôi phục note đã xoá (từ trash).
    

### 2.2 Tìm kiếm & Lọc

- Full-text search trong tiêu đề & nội dung.
    
- Lọc theo tag, folder, thời gian, trạng thái (active/archived/deleted).
    
- Sắp xếp theo ngày tạo, ngày cập nhật, tên.
    

### 2.3 Tổ chức & Phân loại

- Tags/labels: nhiều tag cho một note.
    
- Màu sắc phân loại note.
    
- Folder/Project grouping.
    
- Pin/Favorite notes.
    
- Archive notes.
    

### 2.4 Rich Text / Multimedia

- Hỗ trợ format văn bản (bold, italic, checklist, heading, code block).
    
- Đính kèm: hình ảnh, link, file PDF, video.
    
- Drag & drop upload.
    

### 2.5 Quản lý Thời gian & Nhắc nhở

- Deadline cho note.
    
- Reminder (one-time / recurring).
    
- Push notification + email reminder.
    

### 2.6 Đồng bộ & Bảo mật

- Lưu trữ cloud (database backend).
    
- Offline mode + auto sync khi có mạng.
    
- Mã hoá nội dung note riêng tư (optional per-note).
    

### 2.7 Chia sẻ & Cộng tác

- Share note (read-only / edit).
    
- Comment / reaction.
    
- Mention user `@username`.
    
- Real-time collaborative editing (optional advanced).
    

---

## 3. Yêu cầu kỹ thuật

### 3.1 Database (SQL)

**Table: notes**

- id (PK)
    
- title (varchar)
    
- content (text/json - rich text)
    
- color (varchar, nullable)
    
- pinned (boolean, default false)
    
- archived_at (datetime, nullable)
    
- deleted_at (datetime, nullable)
    
- created_at (datetime)
    
- updated_at (datetime)
    
- user_id (FK → users.id)
    

**Table: tags**

- id (PK)
    
- name (varchar)
    
- color (varchar)
    

**Table: note_tags**

- note_id (FK → notes.id)
    
- tag_id (FK → tags.id)
    

**Table: reminders**

- id (PK)
    
- note_id (FK → notes.id)
    
- remind_at (datetime)
    
- type (enum: once, daily, weekly, monthly)
    

**Table: attachments**

- id (PK)
    
- note_id (FK → notes.id)
    
- file_url (varchar)
    
- file_type (varchar)
    
- created_at (datetime)
    

**Table: shares (nếu có cộng tác)**

- id (PK)
    
- note_id (FK → notes.id)
    
- shared_with_user_id (FK → users.id)
    
- permission (enum: read, edit)
    

---

### 3.2 API Endpoints (REST)

#### Notes

- `POST /api/notes` → tạo note
    
- `GET /api/notes` → danh sách (filter, search, sort)
    
- `GET /api/notes/{id}` → chi tiết note
    
- `PUT /api/notes/{id}` → cập nhật note
    
- `DELETE /api/notes/{id}` → xoá (soft delete → trash)
    
- `PATCH /api/notes/{id}/restore` → khôi phục
    

#### Tags

- `POST /api/tags` → tạo tag
    
- `GET /api/tags` → danh sách tag
    
- `POST /api/notes/{id}/tags` → gắn tag cho note
    

#### Reminders

- `POST /api/notes/{id}/reminder` → thêm nhắc nhở
    
- `DELETE /api/reminders/{id}` → xoá reminder
    

#### Attachments

- `POST /api/notes/{id}/attachments` → upload file
    
- `DELETE /api/attachments/{id}` → xoá file
    

#### Share & Collaboration

- `POST /api/notes/{id}/share` → chia sẻ note
    
- `GET /api/notes/{id}/comments` → list comment
    
- `POST /api/notes/{id}/comments` → thêm comment
    

---

### 3.3 Logic

- **Search**: ElasticSearch hoặc PostgreSQL `tsvector`.
    
- **Reminder**: cron job hoặc push notification service.
    
- **Sync**: WebSocket cho real-time; fallback = polling.
    
- **Offline Mode**: localStorage/IndexedDB cache.
    
- **Security**: RBAC cho note sharing, AES encryption cho private notes.
    

---

## 4. UI/UX

- **Sidebar**: danh sách note, folder, tag filter.
    
- **Main Content**: rich-text editor (giống Notion/Google Keep).
    
- **Topbar**: search bar, toggle dark/light mode.
    
- **Note Card**: tiêu đề, preview, tags, color.
    
- **Quick Note Button**: floating action button (FAB).
    
- **Trash View**: phục hồi/xoá vĩnh viễn.
    
- **Dashboard Widget**: hiển thị recent notes.
    

---

## 5. Đề xuất mở rộng

- AI tóm tắt note / gợi ý tag.
    
- Export note ra PDF/Markdown/Share Link.
    
- Versioning (lịch sử chỉnh sửa).
    
- Templates (Checklist, Meeting Notes, To-do).
    
- Voice-to-text input.
    
- Global Search (search toàn hệ thống, bao gồm notes).
    

---

## 6. Gợi ý phát triển tương lai

- Mobile App (React Native/Flutter).
    
- Tích hợp với Google Calendar/Outlook.
    
- AI Chat: tìm kiếm note bằng ngôn ngữ tự nhiên.
    
- Analytics: thống kê số lượng note, tag sử dụng nhiều.





















