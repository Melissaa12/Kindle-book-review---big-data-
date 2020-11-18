sudo apt update
sudo apt-get update
sudo apt install libcurl3
sudo apt-get install -y debconf-utils

sudo DEBIAN_FRONTEND=noninteractive
echo "mysql-server mysql-server/root_password password pass" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password pass" | sudo debconf-set-selections
sudo apt-get -y install mysql-server
sudo apt-get -y install zip unzip
ssh -o StrictHostKeyChecking=no ubuntu@$1 -i /Users/ryan/Desktop/DBProject/dbproject.pem
echo "now go to mysql"
wget https://istd50043.github.io/assets/scripts/get_data.sh
chmod +x get_data.sh
./get_data.sh
sudo mysql -u root -ppass  
show databases;
create database if not exists books;
show databases;
use books;

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



LOAD DATA LOCAL INFILE 'kindle_reviews.csv' IGNORE INTO TABLE kindle
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SELECT COUNT(asin) FROM books.kindle;

CREATE TABLE `books`.`reviewers` (
  `reviewerID` VARCHAR(45) NOT NULL,
  `reviewerName` LONGTEXT NULL,
  PRIMARY KEY (`reviewerID`));

INSERT INTO `reviewers` (`reviewerID`, `reviewerName`)
SELECT `reviewerID`, `reviewerName` FROM `kindle`
ON DUPLICATE KEY UPDATE 
  `reviewerName` = VALUES(`reviewerName`);

SELECT COUNT(reviewerID) FROM books.reviewers;