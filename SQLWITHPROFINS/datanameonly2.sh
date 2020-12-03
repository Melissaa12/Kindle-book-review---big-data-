# sudo su root
# sudo chown hadoop .ssh
# sudo chown hadoop .ssh/authorized_keys
sudo su hadoop
cd ..
cd hadoop
cat .ssh/id_rsa.pub >> .ssh/authorized_keys