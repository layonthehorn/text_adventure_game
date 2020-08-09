echo "Setting up VENV."
python3 -m venv %~dp0..\env

echo "Updating pip"
%~dp0..\env\bin\pip install --upgrade pip

echo "Installing Packages to VENV"
%~dp0..\env\bin\pip install xdg colorama

echo "Setup complete"
pause
