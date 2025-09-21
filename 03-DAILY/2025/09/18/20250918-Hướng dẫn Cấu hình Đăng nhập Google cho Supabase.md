created: 2025-09-18 22:54:14
modified: 2025-09-18 22:54:14
aliases: [2025-09-18]
tags: [daily, 2025-09-18]

---



### **Hướng dẫn Cấu hình Đăng nhập Google cho Supabase (5 phút)**

**Bước 1: Lấy "Callback URL" từ Supabase**

1. Vào trang quản lý dự án Supabase của bạn.
    
2. Đi đến mục **Authentication** -> **Providers**.
    
3. Tìm đến **Google** và nhấn vào đó. Bạn sẽ thấy một trường tên là **Redirect URL (Callback URL)**.
    
4. **Sao chép (Copy) URL này.** Nó sẽ có dạng: https://<mã-dự-án-của-bạn>.supabase.co/auth/v1/callback. Đây là địa chỉ mà Google sẽ gửi người dùng về sau khi họ đăng nhập thành công.
    

**Bước 2: Tạo "Chìa khóa" trên Google Cloud Console**

1. Truy cập [Google Cloud Console](https://www.google.com/url?sa=E&q=https%3A%2F%2Fconsole.cloud.google.com%2F).
    
2. Tạo một dự án mới (New Project) nếu bạn chưa có.
    
3. Vào mục **APIs & Services** -> **Credentials**.
    
4. Nhấn **+ CREATE CREDENTIALS** và chọn **OAuth client ID**.
    
5. Chọn **Application type** là **Web application**.
    
6. Đặt tên cho nó (ví dụ: "Creator Suite App").
    
7. Trong phần **Authorized redirect URIs**, nhấn **+ ADD URI** và **dán cái Callback URL** bạn đã sao chép từ Supabase ở Bước 1 vào đây.
    
8. Nhấn **Create**.
    

Sau khi tạo xong, Google sẽ cung cấp cho bạn 2 thứ cực kỳ quan trọng:

- **Your Client ID**
    
- **Your Client Secret**
    

**Bước 3: Hoàn tất Cấu hình trên Supabase**

1. Quay trở lại trang cấu hình Google Provider trên Supabase (nơi bạn lấy Callback URL).
    
2. **Dán Client ID** của Google vào trường **Client ID**.
    
3. **Dán Client Secret** của Google vào trường **Client Secret**.
    
4. Bật **Enable Google for new users**.
    
5. Nhấn **Save**.
    

Sau khi bạn hoàn thành 3 bước trên, chức năng đăng nhập bằng Google trên ứng dụng của bạn sẽ hoạt động ngay lập tức mà không cần thay đổi bất kỳ dòng code nào.


















