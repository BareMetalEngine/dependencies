# !/bin/bash

if [ "$EUID" -eq 0 ]
  then echo "Please DONT run as root"
  exit
fi

echo Updating...
sudo apt-get update
#sudo apt-get upgrade -y

echo Installing build tools...
sudo apt-get install build-essential clang

echo Installing generic tools...
sudo apt-get install zip xterm perl ninja-build cmake perl

echo Installing libraries...
sudo apt-get install libharfbuzz-dev
sudo apt-get install libxxf86vm-dev
sudo apt-get install libglu1-mesa-dev
sudo apt-get install freeglut3-dev
sudo apt-get install libcg libcggl

echo Installing python...
sudo apt-get install python3 python-is-python3 pip
pip install jinja2