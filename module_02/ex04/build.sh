#!/bin/bash

# bash script that builds our package

# Install pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Build the distribution files
python3 setup.py sdist bdist_wheel

# Install the package from the local distribution files
pip install ./dist/my_minipack-*.tar.gz




# Cannot activate the venv in Powershell?
# Simply open a Powershell window as administrator and type the following:
#       PS C:\> Set-ExecutionPolicy RemoteSigned
# And hit enter, respond y to any prompts that appear.
# To revert the changes, type the following:
#       PS C:\> Set-ExecutionPolicy Restricted
#
# WSL2 requires to enable Windows Optional Features: "Virtual Machine Platform"
# (Go to Settings\Apps\Optional Features\More Windows Features\VirtualMachinePlatform)
#
# Installing venv in WSL2(Ubuntu):
#
# sudo apt-get update
# sudo apt-get install libpython3-dev
# sudo apt-get install python3-venv
# python3 -m venv <env_anme>
#
