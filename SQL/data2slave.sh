#!/bin/bash
#THIS IS FOR slave DATA SETUP2
echo i have entered $2


sudo tee /home/ubuntu/hadoop-3.3.0/etc/hadoop/slaves << EOF
${2}
EOF

