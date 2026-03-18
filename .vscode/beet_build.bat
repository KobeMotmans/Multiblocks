@echo off
setlocal


echo === TRY PC1 VENV ===
call :run_in_venv ".venv_pc1"
if %errorlevel%==0 goto end


echo === TRY PC2 VENV ===
call :run_in_venv ".venv_pc2"
if %errorlevel%==0 goto end


echo === FALLBACK VENV ===
call :fallback_venv
if %errorlevel%==0 goto end

echo [FATAL] Geen enkele venv kon succesvol runnen.
exit /b 1


:end
echo Klaar!
exit /b 0



REM =================================================
REM  FUNCTIE: RUN BINNEN EEN VENV (TRY/CATCH SIMULATIE)
REM =================================================
:run_in_venv
set "VENV=%~1"

if not exist %VENV% (
    echo [INFO] %VENV% bestaat niet — skip
    exit /b 1
)

echo [INFO] Activating: %VENV%
call %VENV%\Scripts\activate.bat || (
    echo [ERROR] Kan venv niet activeren
    exit /b 1
)

echo [INFO] Running beet...
beet --log debug || (
    echo [ERROR] beet faalde
    exit /b 1
)

echo [INFO] Running done_sound.py...
py done_sound.py || (
    echo [ERROR] done_sound.py faalde
    exit /b 0
)

echo [OK] %VENV% succesvol gebruikt.
exit /b 0



REM =================================================
REM  FALLBACK FUNCTIE 
REM =================================================
:fallback_venv
if not exist .venv (
    echo [INFO] Nieuwe fallback venv maken...
    py -m venv .venv || exit /b 1
)
echo [INFO] Fallback venv activeren...
call .venv\Scripts\activate.bat || exit /b 1

echo [INFO] Requirements installeren...
pip install -r requirements.txt || exit /b 1

echo [INFO] Running beet...
beet --log debug || exit /b 1

echo [INFO] Running done_sound.py...
py done_sound.py || exit /b 0

echo [OK] Fallback succesvol.
exit /b 0