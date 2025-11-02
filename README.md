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
**Frontend:** ![HTML5](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css&logoColor=white) ![JavaScript](https://img.shields.io/badge/Javascript-ffea00?style=for-the-badge&logo=javascript&logoColor=black) ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

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

*   Python 3.x
*   pip (trình quản lý gói cho Python)
*   Node.js
*   npm (trình quản lý gói cho Node.js)
*   Git

### Các bước cài đặt

#### Đối với Windows:

1.  Mở Command Prompt hoặc PowerShell.
2.  Tạo 1 file `setup.bat` và copy nội dung sau:
    ```bash
    @echo off
    echo Cloning repository...
    git clone https://github.com/lequochuy12012k4/HTY-Company
    echo Installing Python requirements...
    pip install -r requirements.txt
    echo Migrate to database
    python manage.py makemigrations
    python manage.py migrate
    echo Setup complete.
    echo Server is running at http://127.0.0.1:8000/
    python manage.py runserver
    pause
    ```

#### Đối với macOS và Linux:

1.  Mở Terminal.
2.  Tạo 1 file `setup.sh` và copy nội dung sau:
    ```bash
    echo "Cloning repository..."
    git clone https://github.com/lequochuy12012k4/HTY-Company
    echo "Changing directory to HTY-Company..."
    cd HTY-Company
    echo "setup virtual enviroment"
    python -m venv .venv
    source .venv/bin/activate
    echo "Installing Python requirements..."
    pip install -r requirements.txt
    echo Migrate to database
    python manage.py makemigrations
    python manage.py migrate
    echo Setup complete.
    echo Server is running at http://127.0.0.1:8000/
    python manage.py runserver
    ```
2.  Cấp quyền thực thi cho file `setup.sh` (chỉ cần làm một lần):
    ```bash
    chmod +x setup.sh
    ```
3.  Chạy file `setup.sh`:
    ```bash
    ./setup.sh
    ```

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
