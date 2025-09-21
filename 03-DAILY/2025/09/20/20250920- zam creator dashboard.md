created: 2025-09-20 00:12:56
modified: 2025-09-20 00:12:56
aliases: [2025-09-20]
tags: [daily, 2025-09-20]

---

#youtube/zam/tools/dashboard
## 🧩 Tính năng
# 📑 Tài liệu yêu cầu hệ thống: Prompt Manager

**Ngày cập nhật:** 2025-09-20

---

## 🧩 Tính năng chính

1. **Prompt Manager**
    
    - Giao diện đa dạng: **Card view / List view / Grid view** (user có thể toggle).
        
    - Bộ lọc theo **tag / category / source**.
        
    - Tích hợp với các nguồn bên ngoài (OpenPrompt, Prompt Marketplace, App Marketplace...).
        
    - Cho phép **link sang trang gốc** hoặc **embed nội dung prompt** trực tiếp.
        
    - Hỗ trợ **AI Assist** để gợi ý, tối ưu và phân loại prompt.
        
2. **Prompts CRUD (`/prompts`)**
    
    - Tạo / Đọc / Cập nhật / Xóa prompt.
        
    - Tìm kiếm nâng cao + lọc (theo tên, tag, category, author, ngày tạo, độ phổ biến...).
        
3. **Công cụ tích hợp**
    
    - Copy nhanh (one-click copy).
        
    - Share link.
        
    - Export (JSON, Markdown).
        
    - Embed iframe/script.
        

---

## ⚙️ Yêu cầu kỹ thuật

### Backend

- **Model Prompt**
    
    `{   "id": "uuid",   "title": "string",   "description": "string",   "content": "string",   "tags": ["string"],   "category": "string",   "source": "string (internal | openprompt | marketplace | custom)",   "source_url": "string | null",   "is_embedded": "boolean",   "created_at": "datetime",   "updated_at": "datetime",   "created_by": "user_id" }`
    
- **API endpoints**
    
    - `GET /prompts` → list + filter + search.
        
    - `GET /prompts/{id}` → chi tiết.
        
    - `POST /prompts` → tạo mới.
        
    - `PUT /prompts/{id}` → cập nhật.
        
    - `DELETE /prompts/{id}` → xóa.
        
    - `POST /prompts/assist` → AI Assist (gợi ý tag, cải thiện prompt, tìm tương tự).
        

### Frontend

- **UI linh hoạt**:
    
    - Card/List/Grid view (toggle).
        
    - Responsive layout (desktop, tablet, mobile).
        
- **Tích hợp công cụ quen thuộc**: Copy, Export, Embed, Share.
    
- **AI Assist Panel**: gợi ý cải thiện prompt, tag/category, prompt tương tự.
    

---

## 💡 Đề xuất mở rộng

- **Rating / Like / Bookmark** cho prompt.
    
- **Version control**: lưu history, revert.
    
- **Import/Export** (JSON, CSV, share link).
    
- **AI auto-tagging** khi tạo prompt.
    
- **Dark mode / Light mode**.
    
- **Customizable layout** (kéo-thả sắp xếp).
    
- **Keyboard shortcut** cho thao tác nhanh.
    
- **Plugin system** (Notion, Obsidian, Google Docs...).
    

---

## 🎨 Gợi ý UI/UX

- **Topbar**: Search bar + toggle view (card/list/grid).
    
- **Sidebar**: Bộ lọc theo tag/category/source, toggle “AI Assist”.
    
- **Card View**: modern UI, soft shadow, icon theo category, tag chips.
    
- **List View**: hiển thị thông tin nhanh gọn, nút action.
    
- **Grid View**: dạng gallery, duyệt nhiều prompt một lúc.
    
- **Detail View**: editor (Markdown/code), metadata (tags, category, source, author), actions (Copy, Embed, Share).
    
- **AI Assist Panel (slide từ cạnh phải)**:
    
    - Gợi ý cải thiện prompt.
        
    - Gợi ý tag/category.
        
    - Đề xuất prompt liên quan.
        

---

## 🔮 Gợi ý tương lai

- **Recommendation Engine**: gợi ý prompt phổ biến/tương tự.
    
- **Marketplace Integration**: cho phép mua/bán prompt cao cấp.
    
- **AI Assist nâng cao**: tối ưu prompt đa ngôn ngữ, auto rewrite.
    
- **Real-time collaboration**: nhiều người cùng chỉnh sửa.
    
- **AI Auto-organizer**: gom nhóm prompt theo ngữ nghĩa.