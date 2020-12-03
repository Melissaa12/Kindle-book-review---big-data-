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