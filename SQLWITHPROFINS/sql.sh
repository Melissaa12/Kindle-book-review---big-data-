#installing dependencies
sudo apt update
sudo apt-get update
sudo apt install libcurl3
sudo apt-get install -y debconf-utils

sudo DEBIAN_FRONTEND=noninteractive
echo "mysql-server mysql-server/root_password password pass" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password pass" | sudo debconf-set-selections
sudo apt-get -y install mysql-server
sudo apt-get -y install zip unzip
ssh -o StrictHostKeyChecking=no ubuntu@$1 -i $2

#Downloading data using data.sh
wget https://istd50043.github.io/assets/scripts/get_data.sh
chmod +x get_data.sh
./get_data.sh

#setting SQL config
echo "Updating mysql configs in /etc/mysql/my.cnf."

sudo tee /etc/mysql/my.cnf << EOF
[mysqld]
bind-address    = 0.0.0.0

!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/

EOF

sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf

echo "Updated mysql bind address in /etc/mysql/my.cnf to 0.0.0.0 to allow external connections."
#Restart to flush changes
sudo /etc/init.d/mysql stop
sudo /etc/init.d/mysql start

#log into sql user and creates the database,table and fills the table with all data
sudo mysql -u root -ppass  
show databases;
create database if not exists books;
show databases;
use books;

CREATE TABLE `books`.`kindle` (
  `idx` INT NOT NULL AUTO_INCREMENT,
  `asin` VARCHAR(45) NOT NULL,
  `helpful` VARCHAR(45) NULL,
  `overall` INT(11) NULL,
  `reviewText` LONGTEXT NULL,
  `reviewerTime` VARCHAR(45) NULL,
  `reviewerID` VARCHAR(45) NULL,
  `reviewerName` LONGTEXT NULL,
  `summary` LONGTEXT NULL,
  `unixReviewTime` VARCHAR(45) NULL,
  PRIMARY KEY (`idx`));



LOAD DATA LOCAL INFILE 'kindle_reviews.csv' IGNORE INTO TABLE kindle
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SELECT COUNT(asin) FROM books.kindle;

#Create table and populate data for only reviewer and reviwerID
CREATE TABLE `books`.`reviewers` (
  `reviewerID` VARCHAR(45) NOT NULL,
  `reviewerName` LONGTEXT NULL,
  PRIMARY KEY (`reviewerID`));

INSERT INTO `reviewers` (`reviewerID`, `reviewerName`)
SELECT `reviewerID`, `reviewerName` FROM `kindle`
ON DUPLICATE KEY UPDATE 
  `reviewerName` = VALUES(`reviewerName`);

SELECT COUNT(reviewerID) FROM books.reviewers;

#Create Another user for external connections like for the flask frontend
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'bookreviewer';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
CREATE USER 'admin'@'%' IDENTIFIED BY 'bookreviewer';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

