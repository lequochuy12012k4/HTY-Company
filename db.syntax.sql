-- Query 1: Get the top 5 most favorited documents, along with their author and the number of favorites.
SELECT
    d.title AS document_title,
    a.name AS author_name,
    COUNT(df.user_id) AS favorite_count
FROM
    app_document d
JOIN
    app_author a ON d.author_id = a.id
LEFT JOIN
    app_document_favorited_by df ON d.id = df.document_id
GROUP BY
    d.id, a.id
ORDER BY
    favorite_count DESC
LIMIT 5;

-- Query 2: Get the number of documents uploaded by each user in each department.
SELECT
    u.username,
    d.name AS department_name,
    COUNT(doc.id) AS document_count
FROM
    auth_user u
JOIN
    app_profile p ON u.id = p.user_id
JOIN
    app_department d ON p.department_id = d.id
LEFT JOIN
    app_document doc ON u.id = doc.user_id AND d.id = doc.department_id
GROUP BY
    u.id, d.id
ORDER BY
    u.username, department_name;

-- Query 3: Get the list of users who have not uploaded any documents.
SELECT
    u.username
FROM
    auth_user u
LEFT JOIN
    app_document d ON u.id = d.user_id
WHERE
    d.id IS NULL;
