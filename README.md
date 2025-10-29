<table>
  <tr>
    <td width="100" valign="middle">
      <img src="app/static/images/icontab.png" alt="Logo ứng dụng" width="100">
    </td>
    <td valign="middle">
      <h1>Ứng dụng Web Quản lý tài liệu nội bộ Công ty</h1>
    </td>
  </tr>
</table>

## Link Website: <a href="https://hty-company.com" target="_blank">hty-company.com</a>

<p>Do website không thể chạy 24/7 nên khi nào cần thì bạn có thể liên hệ tôi qua: </p>

<table>
  <tr>
    <td style="vertical-align: middle;"><a href="https://www.facebook.com/lequochuy12012k4" target="_blank">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook">
  </a></td>
    <td style="vertical-align: middle; padding-left: 10px;"><strong style="font-size: 1.5em;">Lê Quốc Huy</strong></td>
  </tr>
  <tr>
    <td style="vertical-align: middle;"><a href="mailto:lequochuy12012k4@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a></td>
    <td style="vertical-align: middle; padding-left: 10px;"><strong style="font-size: 1.5em;">lequochuy12012k4@gmail.com</strong></td>
  </tr>
</table>

## Giới thiệu

Đây là một ứng dụng web được xây dựng bằng Django, cho phép người dùng quản lý, tải lên, và chia sẻ tài liệu. Ứng dụng cung cấp các tính năng như quản lý tài liệu, tác giả, và cho phép người dùng đánh dấu các tài liệu yêu thích.

## Công nghệ sử dụng
**Frontend:** ![HTML5](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

**Backend:** ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

**Database:** ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

**Deloy:** ![Firebase Studio](https://img.shields.io/badge/Firebase%20Studio-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)

## Tính năng chính

*   **Quản lý tài liệu:** Tải lên, xem, và xóa các tài liệu.
*   **Quản lý tác giả:** Thêm và quản lý thông tin tác giả.
*   **Yêu thích:** Người dùng có thể đánh dấu và xem danh sách các tài liệu yêu thích.
*   **Giao diện người dùng:** Giao diện được xây dựng với sự hỗ trợ của Tailwind CSS.

## Hướng dẫn Cài đặt và Chạy ứng dụng

### Yêu cầu hệ thống

*   Python 3.x (tải Python tại <a href="https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe">đây</a>, nhớ tick phần "Add to PATH" khi cài đặt Python)
*   pip (trình quản lý gói cho Python, đã được tải cùng khi tải Python)
*   Node.js (để cài đặt và chạy Tailwind CSS, tải Nodejs tại <a href="https://nodejs.org/dist/v24.9.0/node-v24.9.0-x64.msi">đây</a> )
*   npm (trình quản lý gói cho Nodejs, đã được tải cùng khi tải Nodejs)
*   Git (để clone source code từ Github, tải Git tại <a href="https://git-scm.com/downloads/win">đây</a> )

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
    (Nếu có script build:css trong `package.json` để biên dịch Tailwind CSS)
    ```bash
    npm run build:css
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
*   `hty-companyDB.sqlite3`: File cơ sở dữ liệu SQLite.
*   `requirements.txt`: Danh sách các thư viện Python.
*   `app/`: Thư mục chứa ứng dụng Django chính.
*   `static/`: Thư mục chứa các file tĩnh (CSS, JavaScript, hình ảnh).
*   `templates/`: Thư mục chứa các template HTML.
*   `tailwind.config.js`: File cấu hình cho Tailwind CSS.
*   `package.json`: File định nghĩa các gói và script cho frontend.

## Ghi chú

Folder `ALL IN ONE` được dùng để: 
*   Làm silde thuyết trình
*   Làm file word/pdf
*   Bao gồm:
     *  Các bảng dữ liệu
     *  EDR
     *  Lược đồ quan hệ
     *  Phân tích mức độ chuẩn hóa 
     *  Rằng buộc chọn vẹn

## Cảm ơn

Cảm ơn bạn đã ghé thăm. Nếu bạn có bất kỳ câu hỏi hoặc góp ý nào, xin vui lòng liên hệ với tôi!

<table>
  <tr>
    <td style="vertical-align: middle;"><a href="https://www.facebook.com/lequochuy12012k4" target="_blank">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook">
  </a></td>
    <td style="vertical-align: middle; padding-left: 10px;"><strong style="font-size: 1.5em;">Lê Quốc Huy</strong></td>
  </tr>
  <tr>
    <td style="vertical-align: middle;"><a href="mailto:lequochuy12012k4@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a></td>
    <td style="vertical-align: middle; padding-left: 10px;"><strong style="font-size: 1.5em;">lequochuy12012k4@gmail.com</strong></td>
  </tr>
</table>