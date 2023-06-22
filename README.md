# top_traders


mysql -u root -p
CREATE USER 'admin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin'; 
GRANT SELECT, UPDATE, DELETE,INSERT ON top_traders_deals.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;

