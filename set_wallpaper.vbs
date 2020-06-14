Set ws = createObject("WScript.shell")
ws.run "cmd /c C:\Users\jared\AppData\Local\Programs\Python\Python38\python.exe  C:\Users\jared\Pictures\photo_of_the_day\set_wallpaper.py > C:\Users\jared\Pictures\photo_of_the_day\output.log.txt 2>&1",vbhide

' If your python path has spaces, save the cmd in the bat,and use the following command
' ws.run "cmd /c C:\Users\jared\Pictures\photo_of_the_day\set_wallpaper.bat",vbhide
' creat set_wallpaper.bat likes following content:
'   "C:\Users\jared\AppData\Local\Programs\Python\Python38\python.exe"  "C:\Users\jared\Pictures\photo_of_the_day\set_wallpaper.py" > "C:\Users\jared\Pictures\photo_of_the_day\output.log.txt" 2>&1

