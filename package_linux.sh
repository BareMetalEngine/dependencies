# !/bin/bash

# exe checker
function check_bin() {
    if ! hash $1; then
    echo "$1 is not installed" >&2
        exit 1
    else
        echo "$1 is installed"
    fi
}

# python lib checker
function check_pip() {
    pip3 show $1 > /dev/null
    if [ $? -ne 0 ]
    then
        echo "$1 is not installed" >&2
        exit 1
    else
        echo "$1 is installed"
    fi
}

# package checker
function check_lib() {
    dpkg -s $1 > /dev/null
    if [ $? -ne 0 ]
    then
        echo "$1 is not installed" >&2
        exit 1
    else
        echo "$1 is installed"
    fi
}

# command runner
function run_build() {
    python3 build.py -p linux $@
    if [ $? -ne 0 ]
    then
        echo "Building failed" >&2
        exit 2
    fi
}

###############################################

# check if python is installed
if ! hash python3; then
    echo "Python is not installed"
    exit 1
else    
    # check Python version
    ver=$(python3 -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
    if [ "$ver" -lt "30" ]; then
        echo "This script requires python 3.0 or greater"
        exit 1
    else
        echo "Python is installed"
    fi    
fi

# check if required stuff in installed
check_bin clang
check_bin pip
check_bin perl
check_bin ninja
check_bin cmake
check_bin xterm
check_bin zip

# check Python packages
check_pip jinja2

# check if required libraries are installed
check_lib libharfbuzz-dev
check_lib libx11-dev
check_lib libxxf86vm-dev
check_lib libglu1-mesa-dev
check_lib freeglut3-dev
check_lib libcg
check_lib libcggl

# download all libs
run_build pull

# configure and build zlib
#run_build -l zlib pull
run_build -l zlib configure
run_build -l zlib build
run_build -l zlib deploy

# configure and build mbedtls
#run_build -l mbedtls pull
run_build -l mbedtls configure
run_build -l mbedtls build
run_build -l mbedtls deploy

# configure and build all other libs
run_build configure
run_build build
run_build deploy

###############################################

# package the libs
mkdir .artifacts
pushd .out; zip -r ../.artifacts/dependencies_linux.zip .; popd
