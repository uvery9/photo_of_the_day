@echo off
title Get admin rights
mode con cols=100 lines=20
color 3f

:: start Get admin rights
setlocal
set uac=~uac_permission_tmp_%random%
md "%SystemRoot%\system32\%uac%" 2>nul
if %errorlevel%==0 ( rd "%SystemRoot%\system32\%uac%" >nul 2>nul ) else (
	echo set uac = CreateObject^("Shell.Application"^)>"%temp%\%uac%.vbs"
	echo uac.ShellExecute "%~s0","","","runas",1 >>"%temp%\%uac%.vbs"
	echo WScript.Quit >>"%temp%\%uac%.vbs"
	"%temp%\%uac%.vbs" /f
	del /f /q "%temp%\%uac%.vbs" & exit )
endlocal

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
del "%HOMEDRIVE%%HOMEPATH%\Desktop\photo_of_the_day.lnk"

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%HOMEDRIVE%%HOMEPATH%\Desktop\photo_of_the_day.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%EXE_DIR%\photo_of_the_day.exe" >> CreateShortcut.vbs
REM echo oLink.TargetPath = "C:\Users\jared\AppData\Local\photo_of_the_day\photo_of_the_day.exe" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
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

:: copy vbs to startup directory.

set INK_PATH=%HOMEDRIVE%%HOMEPATH%\Desktop\photo_of_the_day.lnk
set LNK_DEST=C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\photo_of_the_day.lnk
set EXE_DIR=%LOCALAPPDATA%\photo_of_the_day
if exist "%LNK_DEST%" (		
		echo file %LNK_DEST% exists
	) else (
		copy %INK_PATH%  "%LNK_DEST%" /y
	)

ping -n 5 127.0.0.1 > nul