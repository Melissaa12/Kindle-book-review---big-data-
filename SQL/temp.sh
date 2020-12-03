sudo apt update
sudo apt-get update
sudo apt install libcurl3
sudo apt-get install -y debconf-utils

sudo DEBIAN_FRONTEND=noninteractive
echo "mysql-server mysql-server/root_password password password" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password password" | sudo debconf-set-selections
sudo apt-get -y install mysql-server
sudo apt-get -y install zip unzip

wget https://istd50043.github.io/assets/scripts/get_data.sh
chmod +x get_data.sh
./get_data.sh

echo "Updating mysql configs in /etc/mysql/my.cnf."

sudo tee /etc/mysql/my.cnf << EOF
[mysqld]
bind-address    = 0.0.0.0

!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/

EOF
sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf

echo "Updated mysql bind address in /etc/mysql/my.cnf to 0.0.0.0 to allow external connections."


sudo /etc/init.d/mysql stop
sudo /etc/init.d/mysql start

sudo mysql -u root -ppass
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'bookreviewer';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
ALTER table kindle_reviews drop column MyUnknownColumn;
FLUSH PRIVILEGES;
CREATE USER 'admin'@'%' IDENTIFIED BY 'bookreviewer';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;”

sudo /etc/init.d/mysql stop
sudo /etc/init.d/mysql start