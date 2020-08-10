$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
cd $ScriptDir
cd ..
if (not Test-Path -Path "env\")
{
    echo "This script requires you to have python3.7 or later installed and on your path."
    echo "This will also launch the game every time so you may continue to use it to play later."
    echo ""
    pause
    python -m venv env
    env\Scripts\activate.ps1
    pip install --upgrade pip
    pip install colorama
    echo "Launching game..."
    pause
}
else
{
    env\Scripts\activate.ps1
    echo "Launching game..."
    pause
}

python .\Vern_Adventures.py
