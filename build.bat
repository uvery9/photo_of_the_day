@echo off
rd /s /q Release
md Release

pyinstaller  -F -i photo_of_the_day.ico photo_of_the_day.py
move /y dist\photo_of_the_day.exe Release\photo_of_the_day_console.exe

pyinstaller  -F -w -i photo_of_the_day.ico photo_of_the_day.py
move /y dist\photo_of_the_day.exe Release\photo_of_the_day.exe

echo "********************built********************"

::clean
echo "********************cleaning temp files********************"
rd /s /q build
rd /s /q __pycache__
del /q photo_of_the_day.spec
rd /s /q dist

echo "********************succeed********************"

pause
