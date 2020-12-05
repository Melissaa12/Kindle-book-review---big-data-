#!/bin/bash
echo mongoip
echo $2
echo sqlipcd
echo $3
echo masterip
echo $4
sudo tee /etc/environment -a <<EOF
WEBIP=${1}
MONGOIP=${2}
SQLIP=${3}
MASTERIP=${4}
EOF

source /etc/environment

echo $MONGOIP
echo $SQLIP
echo $MASTERIP
echo "${WEBIP}:5000"

sudo adduser hadoop --gecos "" --disabled-password
sudo sh -c 'echo "hadoop ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/90-hadoop'
sudo su hadoop
sudo apt-get update
sudo apt-get install git



sudo git clone https://ryangen97:Sherene31071997@github.com/ryangen97/DBProject.git
python3 -V
yes Y|sudo apt install python3-venv
sudo python3 -m venv venv --without-pip --system-site-packages
 . venv/bin/activate
yes Y|sudo apt install python3-pip
echo one
export LC_ALL=C
echo two
pip3 install flask
echo three
yes Y|sudo apt-get install python-pip
echo four
export LC_ALL=C
echo five
pip3 install --upgrade pip
pip3 install numpy
echo six
pip3 install pandas
echo seven
pip3 install pyspark
pip3 install flask-restful
sudo pip3 install pymongo
pip3 install mysql-connector-python-rf
pip3 install bs4
yes "" | sudo add-apt-repository ppa:webupd8team/java
yes Y|sudo apt-get update
yes Y|sudo apt install openjdk-8-jdk

cd DBProject
echo "please enter this in your browser"
echo "${WEBIP}:3306"
echo mongoip
echo $MONGOIP
echo sqlip
echo $SQLIP
echo masterip
echo $MASTERIP
python app.py $MONGOIP $SQLIP $MASTERIP

