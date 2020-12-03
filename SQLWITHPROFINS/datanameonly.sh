sudo su hadoop
echo this is only on the name node
export LC_ALL=C
sudo apt-get install -y ssh
# yes "" | ssh-keygen 
# ssh-keygen -t rsa -N ''
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa

