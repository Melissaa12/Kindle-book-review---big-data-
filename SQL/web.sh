sudo apt-get update
sudo apt-get install git
python3 -V
yes Y|sudo apt install python3-venv
python3 -m venv venv --without-pip --system-site-packages
 . venv/bin/activate
yes Y|sudo apt install python3-pip
export LC_ALL=C
pip3 install flask
git clone https://ryangen97:Sherene31071997@github.com/ryangen97/DBProject.git
cd DBProject
python app.py
echo "please enter this in your browser"
