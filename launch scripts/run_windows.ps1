$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
Set-Location $ScriptDir
Set-Location ..
if ( Test-Path -Path "env\")
{
    env\Scripts\activate.ps1
    Write-Output "Launching game..."

}
else
{
    Write-Output "This script requires you to have python3.7 or later installed and on your path."
    Write-Output "This will also launch the game every time so you may continue to use it to play later."
    Write-Output ""
    pause
    python -m venv env
    env\Scripts\activate.ps1
    pip install --upgrade pip
    pip install colorama
    Write-Output "Launching game..."

}
pause
python .\Vern_Adventures.py
