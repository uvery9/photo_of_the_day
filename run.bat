@echo off

xcopy config.ini Release\ /y /i /q /d /h

cd Release
.\photo_of_the_day_console.exe
if %errorlevel% neq 0 exit /b %errorlevel%
xcopy config.ini ..\ /y /i /q /d /h

rem delay 3s
ping -n 3 127.0.0.1 > nul
