DROP USER IF EXISTS 'ADM'@'localhost';

CREATE USER 'ADM'@'localhost' IDENTIFIED BY 'senha123';

ALTER USER 'ADM'@'localhost' IDENTIFIED WITH mysql_native_password BY 'senha123';

GRANT ALL PRIVILEGES ON *.* TO 'ADM'@'localhost';

FLUSH PRIVILEGES;