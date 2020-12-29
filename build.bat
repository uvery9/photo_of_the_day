@echo off
pyinstaller  -F -w set_wallpaper.py

rd /s /q build
md build
move /y dist\set_wallpaper.exe build\set_wallpaper.exe
echo "********************built********************"

::clean
echo "********************cleaning temp files********************"
rd /s /q __pycache__
del /q set_wallpaper.spec
rd /s /q dist

echo "********************succeed********************"

pause
