#!/usr/bin/env bash


if [ ! -d "../env/" ]; then

  echo "Setting up VENV."
  python3 -m venv ../env

  echo "Updating pip"
  ../env/bin/pip install --upgrade pip

  echo "Installing Packages to VENV"
  ../env/bin/pip install xdg colorama
fi
# this is for setting up the needed VENV on Linux.


echo "Setup complete"
../env/bin/python3 ../Vern_Adventures.py