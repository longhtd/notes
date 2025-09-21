created: 2025-09-20 10:55:56
modified: 2025-09-20 10:55:56
aliases: [2025-09-20]
tags: [daily, 2025-09-20]

---



# 📑 SRD – Ứng dụng tạo video tự động qua Web + Selenium Backend

## 1. Giới thiệu

- **Mục tiêu**: Xây dựng hệ thống cho phép người dùng nhập dữ liệu (kịch bản, Excel, ảnh, tùy chọn mode) ngay trên web UI.
    
- **Cách vận hành**:
    
    - Frontend (web) chỉ lo nhập liệu + hiển thị trạng thái.
        
    - Backend (service) sẽ xử lý job bằng **Selenium automation**, thao tác trực tiếp với VEO3 UI, và gọi **webhook** về hệ thống khi job xong.
        
- **Người dùng mục tiêu**: Content creators, marketer, e-learning.
    

---

## 2. 🧩 Chức năng chính

### 2.1. Nhập liệu trên web

- Form nhập kịch bản (textarea).
    
- Upload file Excel (hỗ trợ nhiều format).
    
- Upload ảnh (optional).
    
- Dropdown chọn **mode** (script-only, script+img, batch…).
    
- Tùy chọn render (chất lượng, giọng đọc, style).
    

### 2.2. Quản lý job

- Khi user nhấn **Generate** → web gửi request `POST /jobs/create`.
    
- Backend trả về **Job ID** + trạng thái ban đầu (`Pending`).
    
- Người dùng theo dõi trạng thái job (`Pending → Running → Done/Failed`).
    

### 2.3. Xử lý backend (Selenium automation)

- Backend service nhận Job → đưa vào queue.
    
- Worker (Selenium runner) chạy:
    
    1. Mở VEO3 UI.
        
    2. Login (session management).
        
    3. Nhập kịch bản / upload Excel / upload ảnh.
        
    4. Chọn mode tương ứng.
        
    5. Click Generate → chờ hoàn tất.
        
    6. Lấy link download / tải video → lưu storage.
        

### 2.4. Webhook callback

- Sau khi job hoàn tất:
    
    - Backend gọi **Webhook URL** mà web đã đăng ký khi tạo job.
        
    - Payload webhook:
        
        `{   "jobId": "uuid",   "status": "done",   "videoUrl": "https://storage.example.com/video123.mp4",   "meta": { "mode": "script+excel" } }`
        
- Web nhận webhook → update UI (job status = Done, hiển thị link video).
    

### 2.5. Dashboard người dùng

- Danh sách job với trạng thái.
    
- Link download / preview video.
    
- Nút “Clone” để nhân bản job (chỉ thay đổi dữ liệu nhỏ).
    

---

## 3. ⚙️ Yêu cầu kỹ thuật

### 3.1. Frontend (Web UI)

- Công nghệ gợi ý: React/Next.js.
    
- Form nhập dữ liệu: script, Excel, ảnh, tùy chọn mode.
    
- Dashboard quản lý job: danh sách + trạng thái + video link.
    
- Gọi API backend qua REST.
    
- Nhận update qua **webhook + polling fallback**.
    

### 3.2. Backend Service

- Công nghệ gợi ý: Python (FastAPI) hoặc Node.js (Express/NestJS).
    
- Chức năng:
    
    - Nhận job (`POST /jobs/create`).
        
    - Quản lý queue (Celery/RQ/Redis queue).
        
    - Chạy Selenium runner.
        
    - Gọi webhook callback.
        
- Lưu metadata job trong Postgres.
    

### 3.3. Automation Layer (Selenium/Playwright)

- Script thao tác trên VEO3 UI (login, nhập dữ liệu, generate).
    
- Cấu hình chạy song song (multi-instance).
    
- Quản lý session để tránh login nhiều lần.
    

### 3.4. Storage

- Video thành phẩm lưu S3-compatible storage.
    
- Trả link download qua webhook.
    

### 3.5. API endpoints

- `POST /jobs/create`
    
    `{   "script": "Xin chào...",   "excelFileUrl": "https://...",   "images": ["host.png"],   "mode": "script+img",   "webhookUrl": "https://myapp.com/webhook/job" }`
    
- `GET /jobs/{id}` → trả trạng thái.
    
- `POST /jobs/{id}/cancel` → hủy job.
    

---

## 4. 🎨 UI/UX gợi ý

- **Trang nhập liệu**
    
    - Text area: kịch bản.
        
    - Upload Excel, ảnh.
        
    - Dropdown chọn mode.
        
    - Nút Generate.
        
- **Trang Dashboard**
    
    - Danh sách job (ID, mode, status).
        
    - Progress bar.
        
    - Link preview/download khi Done.
        
- **Webhook update**
    
    - Khi có webhook callback → frontend update realtime (hoặc qua polling fallback).
        

---

## 5. 💡 Đề xuất mở rộng

- Cho phép **multi-user** (tài khoản, quota).
    
- Tích hợp **Google Sheet** ngoài Excel.
    
- Hỗ trợ **retry job** khi fail.
    
- Hỗ trợ **multi-output** (một video xuất nhiều format: 16:9, 9:16).
    
- Có **rate-limit** để bảo vệ backend.
    

---

## 6. 🔮 Hướng phát triển tương lai

- Thay Selenium bằng **API native** khi có.
    
- Thêm **message queue** (Kafka/RabbitMQ) để scale lớn.
    
- Dùng **Headless browser pool** để giảm chi phí.
    
- Thêm **monitoring dashboard** (Prometheus/Grafana).


















