# 开机设置每日必应/每日聚焦/国家地理为桌面壁纸



中国国家地理的每日一图质量太差，默认不设置。

### 一. 功能:

开机更换国家地理/每日必应/每日聚焦 每日一图为桌面背景,如果解析失败,下载失败,不会修改当前壁纸.

http://www.ngchina.com.cn/photography/photo_of_the_day/

https://cn.bing.com/

"C:\\Users\\\$USERNAME\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_$HASH\\LocalState\\Assets"


### 二. 依赖:
python3

https://www.python.org/downloads/

#### python依赖:
urllib.request
requests
re
os
ctypes
random

shutil
imghdr
Pillow
time



### 三. 更简单的使用方法

运行 cp_exe_to_startup_dir.bat, 会将 Release\set_wallpaper_noconsole.exe 复制到Windows启动文件夹中,**Enjoy it!!!**

注意: 如果杀毒软件拦截,请信任bat脚本行为+软件的安全.

如果不放心,可以自己生成exe文件,自行复制到启动文件夹中.



具体操作如下:


#### 1.运行set_wallpaper.py,看是否能够成功.

在cmd命令窗口下,使用

python set_wallpaper.py

定位修改问题



#### 2. 生成二进制文件

见 build.bat 生成set_wallpaper_noconsole.exe



#### 3. 拷贝到启动文件夹

见 cp_exe_to_startup_dir.bat




### 四. 另外一种使用方法(废弃)

#### 1.新建 set_wallpaper.vbs

格式如下：

Set ws = createObject("WScript.shell")
ws.run "cmd /c C:\Users\jared\AppData\Local\Programs\Python\Python38-32\python.exe  D:\jared\coding\photo_of_the_day\set_wallpaper.py > D:\jared\coding\photo_of_the_day\output.log.txt 2>&1",vbhide

其中,包括
1) python.exe的完整路径

2) set_wallpaper.py的完整路径

3) 输出日志的路径,可以不设置



#### 2.将set_wallpaper.vbs添加到开机启动项
复制set_wallpaper.vbs到路径:
	C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp



###                                                       五. FAQ

如果生成的安全软件报毒,

自己使用build.bat生成.

具体干了哪些事,可以看得到.


