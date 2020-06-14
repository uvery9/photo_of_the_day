# 开机设置国家地理/每日必应每日一图为桌面壁纸

### 功能:

开机更换国家地理/每日必应 每日一图为桌面背景,如果解析失败,下载失败,不会修改当前壁纸.

如果已经下载,也不会重复设置壁纸.

http://www.ngchina.com.cn/photography/photo_of_the_day/

https://cn.bing.com/


### 依赖:

python3

#### python依赖:

urllib
ctypes
requests


### 使用方法

#### 1.安装Python3

https://www.python.org/downloads/



#### 2.修改set_wallpaper.py的图片存储路径

ngc = NgChina(path= u"C:\\Users\\jared\\Pictures\\NGC_photo_of_the_day")



#### 3.运行set_wallpaper.py,看是否能够成功.

在cmd命令窗口下,使用

C:\Users\jared\AppData\Local\Programs\Python\Python38\python.exe C:\Users\jared\Pictures\NGC_photo_of_the_day\set_wallpaper.py

定位修改问题



#### 3.修改set_wallpaper.vbs中的真实路径

Set ws = createObject("WScript.shell")
 ws.run "cmd /c C:\Users\jared\AppData\Local\Programs\Python\Python38\python.exe C:\Users\jared\Pictures\NGC_photo_of_the_day\set_wallpaper.py > C:\Users\jared\Pictures\NGC_photo_of_the_day\output.log.txt 2>&1",vbhide

其中,包括python.exe的完整路径

set_wallpaper.py的完整路径

输出日志的路径,可以不设置.如果不设置,则简化为

Set ws = createObject("WScript.shell")
 ws.run "cmd /c C:\Users\jared\AppData\Local\Programs\Python\Python38\python.exe C:\Users\jared\Pictures\NGC_photo_of_the_day\set_wallpaper.py ",vbhide



#### 5.将set_wallpaper.vbs添加到开机执行脚本
设置vbs开机执行的参考链接:
​	http://www.ouyaoxiazai.com/soft/stgj/14/3093.html
增加到计划任务中,设置延时,等待笔记本Wifi连接上.


### End.



