#!/usr/bin/env bash

# this is for setting up the needed VENV on Linux.
echo "Setting up VENV."
python3 -m venv ../env

echo "Updating pip"
../env/bin/pip install --upgrade pip

echo "Installing Packages to VENV"
../env/bin/pip install xdg colorama

echo "Setup complete"
