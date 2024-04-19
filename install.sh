#!/bin/sh

# Installation Setup
echo 'WeatherStation'

install_module() {
    # Install packages
    while read package; do sudo apt-get install $package 
    done < packages.txt

    # Install Pip modules
    while read module; do sudo pip install $module --upgrade
    done < modules.txt

}

pingtest=$(ping -c 1 -W 5 8.8.8.8 > /dev/null)
if [ $? -eq 0 ]; then
    echo 'Installing necessary packages and modules...'
    install_module
    echo 'Download complete'
else
    echo 'You are not connected to the internet.'
    echo 'Please connect to the internet to use the application.'
    exit 1
fi

# Deletes Caches
find . -name \*.pyc -delete

exit 0