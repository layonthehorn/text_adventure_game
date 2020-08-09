$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
cd $ScriptDir
cd ..
python -m venv env
.env\Scripts\activate
pip install --upgrade pip
pip install colorama
