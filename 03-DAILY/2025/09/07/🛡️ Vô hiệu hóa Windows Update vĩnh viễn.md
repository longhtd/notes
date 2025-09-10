#productivity/windows  

[ChatGPT - Vô hiệu hóa Windows Update](https://chatgpt.com/c/686f9d8e-9958-800c-bba8-ac96b77627e7)

**Tóm tắt:**

Hướng dẫn chi tiết để tắt hoàn toàn Windows Update trên Windows 10/11 (Pro & Home), đảm bảo không tự bật lại bằng nhiều phương pháp kết hợp.

## Các bước thực hiện

### ✅ Bước 1: Tắt dịch vụ Windows Update hoàn toàn

- Nhấn `Win + R` → gõ `services.msc` → Enter
- Tìm **Windows Update**
- Click phải → Properties
- `Startup type`: chọn **Disabled**
- Nhấn **Stop** nếu nó đang chạy
- Nhấn **Apply** và **OK**

> Tuy nhiên, Windows đôi khi vẫn tự bật lại. Làm thêm các bước dưới để chặn hoàn toàn.

### ✅ Bước 2: Chặn update bằng Group Policy (chỉ có trên Win 10/11 Pro)

- Nhấn `Win + R` → gõ `gpedit.msc` → Enter
- Vào:

- Computer Configuration > Administrative Templates > Windows Components > Windows Update

- Mở **Configure Automatic Updates**
- Chọn **Disabled** → Apply → OK

### ✅ Bước 3: Dùng Registry (nếu dùng Win Home)

- Nhấn `Win + R` → gõ `regedit`
- Vào đường dẫn:

- `HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU`

- Nếu chưa có, tạo lần lượt:

- Key `WindowsUpdate`
- Key con `AU`
- Dword `NoAutoUpdate` với giá trị `1`

### ✅ Bước 4: Chặn các service liên quan đến Update

Ngoài **Windows Update**, tắt thêm:

- `Update Orchestrator Service`
- `Windows Update Medic Service` (cái này sẽ tự bật lại, phải dùng quyền cao hơn)

**Cách tắt vĩnh viễn Medic Service:**

- Phải dùng phần mềm như **Windows Update Blocker** hoặc chỉnh quyền:

- Mở `services.msc`
- Tìm `Windows Update Medic Service`
- Không tắt được? Làm như sau:

- Tải **PowerRun**: [https://www.sordum.org](https://www.sordum.org)
- Chạy PowerRun → mở `regedit.exe`
- Vào: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WaaSMedicSvc`
- Đổi `Start` = `4` (Disabled)

### ✅ Bước 5 (khuyến nghị): Dùng phần mềm chuyên dụng

- **Windows Update Blocker** – cực hiệu quả

- Tải tại: [https://www.sordum.org/9470/windows-update-blocker-v1-8/](https://www.sordum.org/9470/windows-update-blocker-v1-8/)
- Mở phần mềm → Chọn **Disable Updates** → Apply Now

---

**Lưu ý:** Một số bản cập nhật bảo mật rất quan trọng, nên cân nhắc nếu dùng máy online thường xuyên. Khi muốn bật lại, chỉ cần đổi lại các giá trị regedit hoặc dùng lại phần mềm.