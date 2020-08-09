$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
cd $ScriptDir
cd ..
python -m venv env
env\Scripts\activate.ps1
pip install --upgrade pip
pip install colorama
pause

python .\Vern_Adventures.py