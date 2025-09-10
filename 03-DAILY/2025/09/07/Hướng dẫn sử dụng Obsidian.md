---
created: 2025-09-01 11:35:03
modified: 2025-09-01 11:35:03
aliases:
  - 2025-09-01
tags:
  - daily
---

# Daily Journal - 2025-09-01

🗓 **Date**: 2025-09-01  
⏰ **Time**: 11:35:03  
📅 **Day**: thứ hai  

---

## 🎯 Goals for Today
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## 📝 Notes & Thoughts
- 
- 
- 
- 

## 🏃‍♂️ Activities
- 
- 
- 
- 

## 📚 Learning
- 
- 
- 
- 


---

## 🏷️ Tags
#daily 
# Hướng dẫn sử dụng Obsidian với cấu trúc khoa học

## 🚀 Bắt đầu nhanh

### 1. Chạy script tạo cấu trúc
```powershell
# Mở PowerShell trong thư mục LeeNotes
.\create_folder_structure.ps1
```

### 2. Mở Obsidian
- Mở Obsidian
- Chọn "Open folder as vault"
- Chọn thư mục LeeNotes

### 3. Cấu hình cơ bản
- Vào Settings → Core plugins
- Bật các plugin cần thiết:
  - Daily notes
  - Templates
  - Graph view
  - Backlinks
  - Tag pane

## 📝 Workflow hàng ngày

### Buổi sáng
1. **Tạo daily note mới**
   - Nhấn `Ctrl+N` hoặc tạo từ template
   - Sử dụng template `01-META/Templates/daily-note.md`

2. **Review tasks từ hôm qua**
   - Kiểm tra các task chưa hoàn thành
   - Chuyển sang hôm nay nếu cần

3. **Plan cho ngày mới**
   - Viết 3 mục tiêu chính
   - Lên danh sách task cần làm

### Trong ngày
1. **Ghi chú nhanh**
   - Sử dụng quick capture
   - Tag ngay lập tức: `#type/idea`, `#type/meeting`

2. **Liên kết notes**
   - Tạo backlinks giữa các note liên quan
   - Sử dụng `[[note name]]` để liên kết

3. **Update progress**
   - Cập nhật task status
   - Ghi lại insights và lessons learned

### Buổi tối
1. **Daily review**
   - Đánh giá những gì đã hoàn thành
   - Ghi lại highlights của ngày

2. **Plan cho ngày mai**
   - Viết 3 task quan trọng nhất
   - Chuẩn bị cho ngày hôm sau

## 🏷️ Hệ thống tagging

### Tags chính
- `#project/active` - Dự án đang thực hiện
- `#project/completed` - Dự án hoàn thành
- `#priority/high` - Ưu tiên cao
- `#priority/medium` - Ưu tiên trung bình
- `#priority/low` - Ưu tiên thấp
- `#status/in-progress` - Đang thực hiện
- `#status/blocked` - Bị chặn
- `#status/done` - Hoàn thành

### Tags theo loại
- `#type/meeting` - Cuộc họp
- `#type/idea` - Ý tưởng
- `#type/learning` - Học tập
- `#type/reference` - Tham khảo
- `#type/journal` - Nhật ký

### Tags theo lĩnh vực
- `#tech/programming` - Lập trình
- `#tech/software` - Phần mềm
- `#business/marketing` - Marketing
- `#business/strategy` - Chiến lược
- `#health/exercise` - Tập thể dục
- `#finance/investment` - Đầu tư

## 🔗 Liên kết và Backlinks

### Tạo liên kết
```markdown
# Liên kết cơ bản
[[Tên note]]

# Liên kết với alias
[[Tên note|Tên hiển thị]]

# Liên kết đến heading
[[Tên note#Heading]]

# Liên kết đến block
[[Tên note#^block-id]]
```

### Sử dụng backlinks
- Xem backlinks trong panel bên phải
- Tạo bi-directional links tự động
- Sử dụng để tìm các note liên quan

## 📊 Sử dụng Graph View

### Cách xem Graph
1. Mở Graph View (Ctrl+G)
2. Sử dụng filters để lọc:
   - Tags
   - Folders
   - File types

### Tips sử dụng Graph
- Zoom in/out để xem chi tiết
- Click vào node để highlight connections
- Sử dụng để tìm clusters của knowledge

## 🎯 Quản lý dự án

### Tạo dự án mới
1. Tạo file trong `02-Projects/Active/`
2. Sử dụng template `project-template.md`
3. Đặt tên: `Project-Name.md`

### Cấu trúc dự án
```markdown
# Project: Tên dự án

## 📋 Overview
- **Status**: In Progress
- **Start Date**: 2024-01-15
- **End Date**: 2024-02-15
- **Priority**: High

## 🎯 Goals
- [ ] Mục tiêu 1
- [ ] Mục tiêu 2

## 📝 Notes
- Ghi chú về dự án

## ✅ Tasks
- [ ] Task 1
- [ ] Task 2

## 📚 Resources
- Link tài liệu
- Reference materials

## 📊 Progress
- 25% hoàn thành
- Milestone 1: Done
- Milestone 2: In Progress
```

## 📚 Quản lý kiến thức

### Tạo note kiến thức
1. Chọn thư mục phù hợp trong `03-Knowledge/`
2. Đặt tên rõ ràng: `Topic-Name.md`
3. Sử dụng tags để phân loại

### Cấu trúc note kiến thức
```markdown
# Tên chủ đề

## 📋 Tóm tắt
Brief overview

## 🔑 Key Points
- Point 1
- Point 2

## 📝 Notes
Detailed notes

## 🔗 Related
- [[Related Topic 1]]
- [[Related Topic 2]]

## 📚 Resources
- Source 1
- Source 2
```

## 📖 Quản lý sách và tài liệu

### Tạo book summary
1. Tạo file trong `04-Resources/Books/`
2. Đặt tên: `Book-Title.md`
3. Sử dụng template book-summary

### Cấu trúc book summary
```markdown
# Tên sách

## 📚 Book Info
- **Author**: 
- **Year**: 
- **Genre**: 
- **Rating**: ⭐⭐⭐⭐⭐

## 📋 Summary
Brief summary

## 🔑 Key Takeaways
- Takeaway 1
- Takeaway 2

## 💬 Quotes
> Quote 1

> Quote 2

## 📝 Notes
Detailed notes

## 🔗 Related Books
- [[Related Book 1]]
- [[Related Book 2]]
```

## 👥 Quản lý mối quan hệ

### Tạo contact note
1. Tạo file trong `05-People/Contacts/`
2. Đặt tên: `Person-Name.md`
3. Ghi thông tin liên hệ và notes

### Cấu trúc contact note
```markdown
# Tên người

## 📞 Contact Info
- **Email**: 
- **Phone**: 
- **LinkedIn**: 
- **Company**: 

## 📝 Notes
- Background
- Interests
- Recent interactions

## 📅 Follow-ups
- [ ] Follow-up task 1
- [ ] Follow-up task 2

## 🔗 Related
- [[Meeting Notes]]
- [[Project Name]]
```

## 🔄 Weekly Review

### Quy trình review hàng tuần
1. **Review daily notes** của tuần
2. **Update project status**
3. **Archive completed tasks**
4. **Plan for next week**
5. **Update goals and priorities**

### Template weekly review
```markdown
# Weekly Review - Week {{week}}

## 📊 This Week
- **Completed**: 
- **In Progress**: 
- **Blocked**: 

## 🎯 Goals Progress
- Goal 1: 
- Goal 2: 

## 📝 Insights
- 

## 🔄 Next Week
- Priority 1: 
- Priority 2: 
- Priority 3: 
```

## 🛠️ Tips và Tricks

### Keyboard shortcuts
- `Ctrl+N`: New note
- `Ctrl+O`: Quick switcher
- `Ctrl+Shift+F`: Search
- `Ctrl+G`: Graph view
- `Ctrl+E`: Toggle edit mode

### Productivity tips
1. **Use templates** cho các loại note thường xuyên
2. **Tag consistently** để dễ tìm kiếm
3. **Link everything** để tạo knowledge network
4. **Review regularly** để keep system clean
5. **Backup often** với cloud sync

### Plugin recommendations
- **Dataview**: Tạo dashboard và queries
- **Calendar**: Xem daily notes theo calendar
- **Kanban**: Quản lý task với board
- **Mind Map**: Tạo mind map từ notes
- **Templater**: Advanced templating

## 🚨 Troubleshooting

### Vấn đề thường gặp
1. **File không sync**: Kiểm tra cloud sync settings
2. **Graph view chậm**: Giảm số lượng files hoặc dùng filters
3. **Template không hoạt động**: Kiểm tra template folder path
4. **Links broken**: Sử dụng Ctrl+O để tìm và fix

### Best practices
1. **Keep it simple**: Bắt đầu đơn giản, phức tạp dần
2. **Be consistent**: Sử dụng naming convention nhất quán
3. **Regular maintenance**: Review và clean up định kỳ
4. **Backup strategy**: Có plan backup rõ ràng
5. **Start small**: Không cần perfect ngay, iterate dần

## 📈 Nâng cao

### Custom CSS
Tạo file `01-META/Config/custom.css` để tùy chỉnh giao diện

### Dataview queries
Sử dụng Dataview plugin để tạo dashboard:
```dataview
LIST FROM #project/active
```

### Automation
- Sử dụng Templater plugin
- Tạo custom scripts
- Integrate với external tools

---

**Lưu ý**: Hệ thống này có thể điều chỉnh theo nhu cầu cá nhân. Bắt đầu với cấu trúc cơ bản và phát triển dần theo thời gian.
