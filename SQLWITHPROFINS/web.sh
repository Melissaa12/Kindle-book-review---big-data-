sudo apt-get update
sudo apt-get install git
echo mongoip
echo $2
echo sqlip
echo $3
echo masterip
echo $4





git clone https://ryangen97:Sherene31071997@github.com/ryangen97/DBProject.git
python3 -V
yes Y|sudo apt install python3-venv
python3 -m venv venv --without-pip --system-site-packages
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
yes "" | sudo add-apt-repository ppa:webupd8team/java
yes Y|sudo apt-get update
yes Y|sudo apt install openjdk-8-jdk

cd DBProject
echo "please enter this in your browser"
echo "$1:5000"
echo mongoip
echo $2
echo sqlip
echo $3
echo masterip
echo $4
python app.py $2 $3 $4

