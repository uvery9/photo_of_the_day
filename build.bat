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

echo "************ copy to LOCALAPPDATA ************"

set EXE_DIR=%LOCALAPPDATA%\photo_of_the_day
if exist "%EXE_DIR%" (		
		echo directory %EXE_DIR% exists
	) else (
		echo make %EXE_DIR%
		%HOMEDRIVE%
		md %EXE_DIR%
	)
cd /d %~dp0
xcopy Release\photo_of_the_day.exe "%EXE_DIR%" /y /i /q /d


echo "************ create lnk ************"
set EXE_DIR=%LOCALAPPDATA%\photo_of_the_day
set INK_FILE=photo_of_the_day.lnk

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "D:\jared\coding\photo_of_the_day\photo_of_the_day.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%EXE_DIR%\photo_of_the_day.exe" >> CreateShortcut.vbs
REM echo oLink.TargetPath = "C:\Users\jared\AppData\Local\photo_of_the_day\photo_of_the_day.exe" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

if exist "%INK_FILE%" (		
		echo file %INK_FILE% exists
	) else (
		cscript CreateShortcut.vbs
	)	
del CreateShortcut.vbs

REM https://superuser.com/questions/392061/how-to-make-a-shortcut-from-cmd
REM Set oWS = WScript.CreateObject("WScript.Shell")
REM sLinkFile = "C:\MyShortcut.LNK"
REM Set oLink = oWS.CreateShortcut(sLinkFile)
REM     oLink.TargetPath = "C:\Program Files\MyApp\MyProgram.EXE"
REM  '  oLink.Arguments = ""
REM  '  oLink.Description = "MyProgram"   
REM  '  oLink.HotKey = "ALT+CTRL+F"
REM  '  oLink.IconLocation = "C:\Program Files\MyApp\MyProgram.EXE, 2"
REM  '  oLink.WindowStyle = "1"   
REM  '  oLink.WorkingDirectory = "C:\Program Files\MyApp"
REM oLink.Save
echo "********************succeed********************"
ping -n 5 127.0.0.1 > nul
