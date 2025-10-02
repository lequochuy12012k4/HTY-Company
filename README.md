<table>
  <tr>
    <td width="100" valign="middle">
      <img src="app/static/images/icontab.png" alt="Logo ứng dụng" width="100">
    </td>
    <td valign="middle">
      <h1>Ứng dụng Web Quản lý Tài liệu</h1>
    </td>
  </tr>
</table>

## Link Website: <a href="https://8000-firebase-hty-company-1757746066281.cluster-w5vd22whf5gmav2vgkomwtc4go.cloudworkstations.dev/" target="_blank">hty-company.com</a>

## Giới thiệu

Đây là một ứng dụng web được xây dựng bằng Django, cho phép người dùng quản lý, tải lên, và chia sẻ tài liệu. Ứng dụng cung cấp các tính năng như quản lý tài liệu, tác giả, và cho phép người dùng đánh dấu các tài liệu yêu thích.

## Công nghệ sử dụng

*   **Frontend:**
    *   ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
    *   ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
    *   ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
    *   ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
*   **Backend:**
    *   ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    *   ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
*   **Database:**
    *   ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

## Tính năng chính

*   **Quản lý tài liệu:** Tải lên, xem, và xóa các tài liệu.
*   **Quản lý tác giả:** Thêm và quản lý thông tin tác giả.
*   **Yêu thích:** Người dùng có thể đánh dấu và xem danh sách các tài liệu yêu thích.
*   **Giao diện người dùng:** Giao diện được xây dựng với sự hỗ trợ của Tailwind CSS.

## Hướng dẫn Cài đặt và Chạy ứng dụng

### Yêu cầu hệ thống

*   Python 3.x
*   pip (trình quản lý gói cho Python)
*   Node.js và npm (để cài đặt và chạy Tailwind CSS)

### Các bước cài đặt

1.  **Clone repository về máy của bạn:**
    ```bash
    git clone https://github.com/lequochuy12012k4/HTY-Company
    ```

2.  **Tạo và kích hoạt môi trường ảo (virtual environment):**
    *   Trên macOS và Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   Trên Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Cài đặt các thư viện Python cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Cài đặt các gói frontend:**
    (Nếu có `package.json`, chạy lệnh sau để cài đặt các gói cần thiết cho frontend, bao gồm Tailwind CSS)
    ```bash
    npm install
    ```

5.  **Thực hiện di chuyển cơ sở dữ liệu (database migrations):**
    Lệnh này sẽ tạo các bảng cần thiết trong cơ sở dữ liệu.
    ```bash
    python manage.py migrate
    ```

6.  **Build các tài sản frontend (frontend assets):**
    (Nếu có script build trong `package.json` để biên dịch Tailwind CSS)
    ```bash
    npm run build
    ```

### Chạy ứng dụng

1.  **Khởi động server phát triển:**
    ```bash
    python manage.py runserver
    ```

2.  **Truy cập ứng dụng:**
    Mở trình duyệt web và truy cập vào địa chỉ `http://127.0.0.1:8000/`.

## Cấu trúc dự án

*   `manage.py`: Script quản lý của Django.
*   `db.sqlite3`: File cơ sở dữ liệu SQLite.
*   `requirements.txt`: Danh sách các thư viện Python.
*   `app/`: Thư mục chứa ứng dụng Django chính.
*   `static/`: Thư mục chứa các file tĩnh (CSS, JavaScript, hình ảnh).
*   `templates/`: Thư mục chứa các template HTML.
*   `tailwind.config.js`: File cấu hình cho Tailwind CSS.
*   `package.json`: File định nghĩa các gói và script cho frontend.
