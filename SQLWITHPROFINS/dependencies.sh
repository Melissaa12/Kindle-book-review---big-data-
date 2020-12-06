yes Y|sudo apt install python3-venv

sudo python3 -m venv venv --without-pip --system-site-packages
export LC_ALL=C
 . venv/bin/activate
yes Y|sudo apt install python-pip3
pip3 install boto3
pip3 install pyyaml
pip3 install --upgrade pip
pip3 install paramiko
