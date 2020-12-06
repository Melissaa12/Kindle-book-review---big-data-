#installing dependencies for sql
sudo apt update
sudo apt-get update
sudo apt install libcurl3
sudo apt-get install -y debconf-utils
sudo DEBIAN_FRONTEND=noninteractive
echo "mysql-server mysql-server/root_password password pass" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password pass" | sudo debconf-set-selections
sudo apt-get -y install mysql-server
sudo apt-get -y install zip unzip

#obtaining data from get_data.sh
ssh -o StrictHostKeyChecking=no ubuntu@$1 -i $2
wget https://istd50043.github.io/assets/scripts/get_data.sh
chmod +x get_data.sh
./get_data.sh

#updating MYSQL configs
sudo tee /etc/mysql/my.cnf << EOF
[mysqld]
bind-address    = 0.0.0.0

!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/

EOF
sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
sudo /etc/init.d/mysql stop
sudo /etc/init.d/mysql start

#log into SQL
sudo mysql -u root -ppass  
show databases;
#Create Database
create database if not exists books;
show databases;
use books;
#Create Main Table
CREATE TABLE `books`.`kindle` (
  `idx` INT NOT NULL,
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


#Loading Data into Table
LOAD DATA LOCAL INFILE 'kindle_reviews.csv' IGNORE INTO TABLE kindle
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SELECT COUNT(asin) FROM books.kindle;
#Create table just for Reviewer Log (reviewerID and ReviewerName)
CREATE TABLE `books`.`reviewers` (
  `reviewerID` VARCHAR(45) NOT NULL,
  `reviewerName` LONGTEXT NULL,
  PRIMARY KEY (`reviewerID`));
#Populate Table from Main Table
INSERT INTO `reviewers` (`reviewerID`, `reviewerName`)
SELECT `reviewerID`, `reviewerName` FROM `kindle`
ON DUPLICATE KEY UPDATE 
  `reviewerName` = VALUES(`reviewerName`);

SELECT COUNT(reviewerID) FROM books.reviewers;
#Create other user for external connections(FrontEnd)
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'bookreviewer';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
CREATE USER 'admin'@'%' IDENTIFIED BY 'bookreviewer';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

