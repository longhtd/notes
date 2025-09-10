#productivity/windows 

[ChatGPT - Tắt cập nhật Windows](https://chatgpt.com/c/686f59d1-3c84-800c-b81b-39a1213cc3c3)

## Tóm tắt

Các cách hiệu quả để tắt cập nhật Windows (Windows Update) trên Windows 10/11, phù hợp cho nhiều mục đích và phiên bản hệ điều hành.

## Highlights

- ✅ **Cách 1: Tắt hoàn toàn bằng Services (Dễ - Nhanh)**

1. Nhấn Win + R > gõ `services.msc` > Enter.
2. Tìm dòng Windows Update > click đúp chuột.
3. Ở mục Startup type > chọn Disabled.
4. Nhấn Stop nếu đang chạy.
5. Bấm Apply > OK.

- ✅ **Cách 2: Dùng Group Policy Editor (chuyên sâu)**

- Áp dụng cho Windows Pro/Education/Enterprise (Home không dùng được)

1. Nhấn Win + R > gõ `gpedit.msc` > Enter.
2. Vào: Computer Configuration > Administrative Templates > Windows Components > Windows Update.
3. Tìm và mở: Configure Automatic Updates.
4. Chọn Disabled > Apply > OK.

- ✅ **Cách 3: Dùng Registry Editor (cho Windows Home)**

- Cẩn thận, sai thao tác dễ lỗi hệ thống

1. Nhấn Win + R > gõ `regedit` > Enter.
2. Điều hướng đến: HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU (Nếu chưa có thư mục WindowsUpdate và AU thì tạo mới).
3. Tạo key DWORD (32-bit) tên: NoAutoUpdate, đặt giá trị = 1.
4. Khởi động lại máy.

- ✅ **Cách 4: Dùng phần mềm bên thứ 3 (an toàn cho người không rành)**

- Windows Update Blocker (gọn nhẹ, dễ dùng)
- StopUpdates10 hoặc Wu10Man

⚠️ **Lưu ý:**

- Tắt cập nhật có thể khiến máy thiếu bản vá bảo mật.
- Nên bật lại định kỳ (1-2 tháng/lần) để kiểm tra update cần thiết.