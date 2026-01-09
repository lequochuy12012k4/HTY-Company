-- Query 1: Liệt kê 5 tài liệu được yêu thích nhất
-- Mục đích: Tìm ra các tài liệu phổ biến nhất dựa trên số lượng người dùng đã yêu thích.
-- Các kỹ thuật SQL: JOIN, GROUP BY, COUNT, ORDER BY, LIMIT
SELECT
    d.title AS TenTaiLieu,
    COUNT(f.id) AS SoLuotYeuThich
FROM
    app_document AS d
JOIN
    app_document_favorited_by AS f ON d.id = f.document_id
GROUP BY
    d.title
ORDER BY
    SoLuotYeuThich DESC
LIMIT 5;

-- Query 2: Tìm người dùng đã tải lên nhiều tài liệu nhất
-- Mục đích: Xác định người dùng đóng góp nhiều nhất cho thư viện tài liệu.
-- Các kỹ thuật SQL: JOIN, GROUP BY, COUNT, ORDER BY, LIMIT
SELECT
    u.username AS TenNguoiDung,
    COUNT(d.id) AS SoTaiLieuTaiLen
FROM
    auth_user AS u
JOIN
    app_document AS d ON u.id = d.user_id
GROUP BY
    u.username
ORDER BY
    SoTaiLieuTaiLen DESC
LIMIT 1;

-- Query 3: Thống kê số lượng tài liệu mà mỗi người dùng đã yêu thích
-- Mục đích: Xem mức độ hoạt động của người dùng trong việc yêu thích tài liệu.
-- Các kỹ thuật SQL: JOIN, GROUP BY, COUNT, ORDER BY
SELECT
    u.username AS TenNguoiDung,
    COUNT(f.document_id) AS SoLuotYeuThich
FROM
    auth_user AS u
JOIN
    app_document_favorited_by AS f ON u.id = f.user_id
GROUP BY
    u.username
ORDER BY
    SoLuotYeuThich DESC;
