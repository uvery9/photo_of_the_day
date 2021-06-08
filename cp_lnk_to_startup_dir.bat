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

:: copy lnk to startup directory.

set INK_NAME=photo_of_the_day.lnk
set LNK_DEST=C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\%INK_NAME%
set EXE_DIR=%LOCALAPPDATA%\photo_of_the_day
if exist "%LNK_DEST%" (		
		echo file %LNK_DEST% exists
	) else (
		cd /d %~dp0
		copy %INK_NAME%  "%LNK_DEST%" /y
	)

ping -n 5 127.0.0.1 > nul
