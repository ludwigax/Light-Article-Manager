setlocal enabledelayedexpansion

call activate pyqt5

for %%f in (*.ui) do (
    set filename=%%~nf
    pyside6-uic %%f -o .\test\!filename!.py
)

echo Conversion complete.