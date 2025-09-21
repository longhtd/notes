created: 2025-09-19 02:28:58
modified: 2025-09-19 02:28:58
aliases: [2025-09-19]
tags: [daily, 2025-09-19]

---

#youtube/zam/tools/dashboard

# 📑 System Requirement Document (SRD v2)

**Hệ thống: Ứng dụng Dashboard hỗ trợ sáng tạo & quản trị nội dung YouTube**

---

## 1. Giới thiệu

Ứng dụng cung cấp nền tảng **all-in-one** cho Content Creator/Team:

- Sinh kịch bản nhanh từ video hoặc transcript.
    
- Quản lý prompt AI.
    
- Quản lý user & phân quyền.
    
- Dashboard quản trị linh hoạt.
    
- App Hub để truy cập nhiều ứng dụng con.
    
- Công cụ Media & Analytics cho YouTube.
    

---

## 2. Các tính năng chính

### 2.1. Sinh kịch bản nhanh từ video YouTube

- Input: link video hoặc playlist.
    
- Fetch transcript (API hoặc upload thủ công).
    
- Sinh kịch bản mới bằng AI (nhiều tone, nhiều version).
    
- Batch generation: nhiều script từ 1 nguồn.
    
- Xuất file: `.txt`, `.md`, `.docx`, `.xlsx`, `.json`.
    

---

### 2.2. Quản lý Prompt & Chế độ sinh kịch bản

- **Auto Mode**: dùng prompt mặc định.
    
- **Manual Mode**: chọn/nhập prompt thủ công.
    
- Prompt Manager: CRUD, gán tag/category, tìm kiếm/lọc.
    
- Prompt history: lưu lại prompt đã dùng với script.
    
- Prompt favorite & default.
    

---

### 2.3. Import & Export Content

- Import: `.txt`, `.md`, `.docx`, `.csv`, `.srt`.
    
- Export: `.txt`, `.md`, `.docx`, `.xlsx` (multi-version), `.json`.
    
- Batch import/export nhiều file.
    
- Export kèm metadata (title, tags, version).
    
- Lưu lịch sử export.
    

---

### 2.4. Hệ thống Login, Quản trị & Phân quyền (RBAC)

- Auth: Email/Password, Google OAuth, reset password.
    
- Role-based Access:
    
    - **Super Admin**: toàn quyền.
        
    - **Content Leader**: quản lý team, duyệt content.
        
    - **Content Writer**: tạo/sửa content cá nhân.
        
    - **Viewer (optional)**: chỉ đọc.
        
- User Manager: CRUD user, gán role, disable, reset password.
    
- Audit Logs: lưu hành động (ai tạo/sửa/xóa).
    

---

### 2.5. Dashboard Quản Trị & Menu Linh Hoạt

- **Dashboard Stats**:
    
    - KPI: số video, số script, user active, prompt phổ biến.
        
    - Biểu đồ: views, script theo thời gian, phân loại category.
        
    - Activity log realtime.
        
- **Sidebar/Menu**:
    
    - Content Manager
        
    - Prompt Manager
        
    - User Manager
        
    - Import/Export Manager
        
    - Audit Logs
        
    - Settings
        
- Tùy biến menu theo role (Super Admin thấy full, Writer chỉ thấy content).
    
- Reorder menu & module.
    

---

### 2.6. App Hub – Quản lý & Truy cập nhiều ứng dụng

- App Hub = trung tâm hiển thị tất cả ứng dụng (grid card/app launcher).
    
- App gồm: Content, Prompt, User, Export, Analytics...
    
- Super Admin bật/tắt app, phân quyền app cho role.
    
- Hỗ trợ external apps (Google Drive, Notion, Slack).
    
- User có thể pin app yêu thích.
    
- Category app (Content Apps, Management Apps, Analytics Apps).
    

---

### 2.7. YouTube Media & Analytics Tools

- **Media Downloader**
    
    - Download thumbnail (nhiều size).
        
    - Download audio (mp3, wav, aac).
        
    - Export metadata (title, desc, tags, category).
        
- **Analytics Fetching**
    
    - Video analytics: views, likes, comments, engagement.
        
    - Channel analytics: subs, total views, growth trend.
        
    - Multi-channel compare: so sánh nhiều kênh/video.
        
- **Export Analytics**
    
    - `.csv` / `.xlsx` (multi-sheet).
        
    - Export batch video/kênh.
        
- **Scheduler** (mở rộng): auto fetch định kỳ.
    

---

## 3. Yêu cầu kỹ thuật

### 3.1. Database Schema (tóm tắt)

- **Users**: id, email, password_hash, role, status, timestamps.
    
- **Roles**: id, role_name, permissions.
    
- **Prompts**: id, title, content, tags, category, is_default, timestamps.
    
- **Videos**: id, youtube_id, title, transcript, category, publish_date.
    
- **Contents**: id, video_id, prompt_id, original, generated, format, version.
    
- **Analytics**: id, video_id, channel_id, views, likes, comments, subscribers, collected_at.
    
- **AuditLogs**: id, user_id, action, target_type, target_id, timestamp.
    
- **Apps**: id, name, description, icon, url_path, category, roles_allowed, status.
    

### 3.2. API Endpoints

- **Auth**: `/auth/login`, `/auth/register`, `/auth/logout`, `/auth/reset-password`.
    
- **Users**: `/users` CRUD.
    
- **Prompts**: `/prompts` CRUD, search/filter.
    
- **Videos**: `/videos/import`, `/videos/{id}/transcript`.
    
- **Content**: `/content/generate`, `/content/import`, `/content/{id}/export`.
    
- **Dashboard**: `/dashboard/stats`, `/dashboard/logs`.
    
- **Menu**: `/menu` get/update.
    
- **Apps**: `/apps` CRUD, `/apps/order`.
    
- **YouTube Media**: `/youtube/video/{id}/thumbnail`, `/youtube/video/{id}/audio`, `/youtube/video/{id}/analytics`, `/youtube/channel/{id}/analytics`, `/youtube/channels/compare`, `/youtube/export`.
    

---

## 4. Gợi ý mở rộng tương lai

- Multi-language script generation.
    
- Collaboration (multi-user editing).
    
- SEO/Trend analysis cho video.
    
- AI Thumbnail Generator.
    
- AI Assistant trong dashboard (hỏi dữ liệu trực tiếp).
    
- Integration export sang YouTube, Notion, Drive.
    
- Marketplace cho Prompt/App.
    
- Gamification cho Writer (leaderboard).
    

---

## 5. UI/UX định hướng

- **Dashboard**: widget grid (stats, charts, logs).
    
- **Sidebar/App Hub**: role-based, grid card launcher, search bar.
    
- **Content Manager**: bảng dữ liệu + filter (user, tag, category).
    
- **Prompt Manager**: card view + tag/category filter.
    
- **User Manager**: table + badge role + quick action.
    
- **Media Tools**: thumbnail preview, audio download, batch actions.
    
- **Analytics Dashboard**: bảng + chart compare video/kênh.
    
- **Export Center**: lịch sử export + tải lại.


















