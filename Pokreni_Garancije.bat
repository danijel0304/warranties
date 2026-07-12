@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_CMD="

where py >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"

if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo Python nije pronaden. Instalirajte Python 3 i pokrenite skriptu ponovno.
    pause
    exit /b 1
)

if exist "requirements.txt" (
    %PYTHON_CMD% -c "import pandas, openpyxl, PIL, pytesseract" >nul 2>nul
    if errorlevel 1 (
        echo Nedostaju Python paketi. Instaliram u korisnicki Python...
        %PYTHON_CMD% -m pip install --user --disable-pip-version-check -r "requirements.txt"
        if errorlevel 1 (
            echo.
            echo Instalacija paketa nije uspjela.
            pause
            exit /b 1
        )
    )
)

echo Pokrecem Garancije...
%PYTHON_CMD% "garancije.py"
set "EXIT_CODE=%errorlevel%"

if not "%EXIT_CODE%"=="0" (
    echo.
    echo Program je zavrsio s greskom: %EXIT_CODE%
    pause
)

exit /b %EXIT_CODE%
