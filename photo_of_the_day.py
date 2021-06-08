# -*- coding: UTF-8 -*-
import urllib.request
import requests
import re
import os
import ctypes
import random

import shutil
import imghdr
from PIL import Image
import time
import configparser

class PyinstallerPath():
    def __init__(self):
        import os, sys
        # determine if the application is a frozen `.exe` (e.g. pyinstaller --onefile) 
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        # or a script file (e.g. `.py` / `.pyw`)
        elif __file__:
            application_path = os.path.dirname(__file__)
        self._getcwd = application_path

class OnlineOrLocalCLS(PyinstallerPath):
    def __init__(self):
        super().__init__()
        self._config_file = os.path.join(self._getcwd, "config.ini")

    def load_config(self, cfg_file):
        raise NotImplementedError('Must be implemented by the subclass')

    def update_element_in_config(self, section, element, element_date, update):
        if update:
            config = configparser.ConfigParser()
            config_file = self._config_file
            if os.path.exists(config_file):
                config.read(config_file)
                config.set(section, element, element_date)
                # os.system( "attrib -h/+h " + config_file) # unhide/hide
                with open(config_file, 'w') as configfile:
                    config.write(configfile)
                print("update \"{}\" = [{}] in config.ini".format(element, element_date))

    def get_online_or_local(self, cfg):
        onlinelocalCfg = cfg['OnlineOrLocal']
        use_photooftheday   = onlinelocalCfg['use_photooftheday']
        use_wallpapersetter = onlinelocalCfg['use_wallpapersetter']
        create_usage_stat   = onlinelocalCfg['create_usage_stat']
        return use_photooftheday, use_wallpapersetter, create_usage_stat

    def creart_def_cfg(self, use_wallpapersetter="no", use_photooftheday="yes", create_usage_stat='twice'):
        config = configparser.ConfigParser()
        if not os.path.exists(self._config_file):
            config['OnlineOrLocal'] = {
                'use_wallpapersetter': use_wallpapersetter,
                'use_photooftheday': use_photooftheday,
                'create_usage_stat': create_usage_stat
            }
            config = self.def_online_cfg(config)
            config = self.def_local_cfg(config)
            with open(self._config_file, 'w') as configfile:
                    config.write(configfile)
            print("Create default config.ini file.")
    
    def def_local_cfg(self, cfg, ngchina='no', bingchina='yes', daily_spotlight='yes', alwaysdl_bing='yes'):
        cfg['WallpaperSetter'] = {
                'img_dir': "C:\\Users\\SOMEONE\\Pictures",
                'copy_folder': "None",
                'want2copy': "no",
                'scan': "yes",
                'mtime': "None",
                'last_img_dir': "None",
                'wallpaper': "C:\\Users\\SOMEONE\\Pictures\\OnePicture.jpeg"
        }
        return cfg

    def def_online_cfg(self, cfg, ngchina='no', bingchina='yes', daily_spotlight='yes', alwaysdl_bing='yes'):
        cfg['PhotoOfTheDay'] = {'ngchina':                       ngchina,
                                'bingchina':                     bingchina,
                                'daily.spotlight':               daily_spotlight,
                                'alwaysdownload.bing.wallpaper': alwaysdl_bing
        }
        return cfg    
    
    @staticmethod
    def set_wallpaper(img_file):
        if os.environ.get("OS") != "Windows_NT":
            print("not Windows, sorry.")
            return None
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDWININICHANGE = 0x02
        ret = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img_file, \
                                                   SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
        if (ret == 0):
            ret = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img_file, 0)
        if (ret == 1):
            print("\n>>>> Set wallpaper succeed! <<<<")
            print("Wallpaper PATH: {}\n".format(img_file))
        else:
            print("\n>>>> Set Wallpaper failed, Try again! <<<<\n")
     
    def create_usage_file(self):
        config = configparser.ConfigParser()
        config_file = self._config_file
        config.read(config_file) 
        a, b, create_usage_stat = self.get_online_or_local(config)
        usage_file = os.path.join(self._getcwd, "USAGE.TXT")
        if not os.path.exists(usage_file) and create_usage_stat.lower() != "no":
            with open(usage_file, 'w', encoding="utf-8") as f:
                f.write(self.get_usage_text())
            print("create USAGE.TXT in path [ {} ]".format(self._getcwd))

            if create_usage_stat.lower() == "twice":
                self.update_element_in_config("OnlineOrLocal", "create_usage_stat", "once", True)
            elif create_usage_stat.lower() == "once":
                self.update_element_in_config("OnlineOrLocal", "create_usage_stat", "no", True) 

    def get_usage_text(self):
# USAGE.TXT
        usage_text = r'''Usage for wallpaper_setter.exe/wallpaper_setter.py
AUTHOR: HDC <jared.dcx@gmail.com>
-----------------------------------------
Notice: there is only ONE file you need to configure: config.ini, 
        it should be with wallpaper_setter.exe/wallpaper_setter.py
-----------------------------------------
here is a sample of config.ini:

[OnlineOrLocal]
use_wallpapersetter = no
use_photooftheday = yes
create_usage_stat = twice

[PhotoOfTheDay]
ngchina = no
bingchina = yes
daily.spotlight = yes
alwaysdownload.bing.wallpaper = yes

[WallpaperSetter]
img_dir = C:\Users\SOMEONE\Pictures
copy_folder = None
want2copy = no
scan = yes
mtime = None
last_img_dir = None
wallpaper = C:\Users\SOMEONE\Pictures\OnePicture.jpeg

---------------------
Section OnlineOrLocal
1. use_wallpapersetter            Download the image and set it as wallpaper.
2. use_photooftheday              Use local image, which means use "Section WallpaperSetter" feature.
3. create_usage_stat              Create and usage file flag: always, once, no
                                    always: when 'USAGE.TXT' doesn't exist, always create
                                    twice:  you can't delete two times
                                    once:   when 'USAGE.TXT' doesn't exist, create once, you can delete, it won't create next time.
                                    no:     literally.
--------
Section PhotoOfTheDay
1. ngchina                        Download "ngchina" 's image and set it as wallpaper
2. bingchina                      Download "bingchina" 's image and set it as wallpaper
3. daily.spotlight                Copy the image from daily.spotlight folder and set it as wallpaper 
                                    [You have to open the feature in Windows10]
4. alwaysdownload.bing.wallpaper  Always download bingchina wallpaper
--------
Section WallpaperSetter
1. img_dir:                       The program will scan this folder and select a image as wallpaper
2. copy_folder:                   Copy all suitable pictures to this folder from copy_folder, control by 'want2copy'
3. want2copy:                     Controlling the action of COPYING, it has two options: yes, no
4. scan:                          Controlling the action of SCANNING, it has three options: yes, no, force
                                    yes:   when 'img_dir' has been modified by OS, scan and update '_img_list.txt'
                                    no:    never scan 'img_dir' unless '_img_list.txt' doesn't exist.
                                    force: Mandatory scan 'img_dir' and update '_img_list.txt'
5. mtime:                         The modified time of 'img_dir'
6. last_img_dir:                  Literally.
7. wallpaper:                     Wallpaper setting history.
-----------------------------------------
FOR FREEDOM!
'''
# ^^^ USAGE.TXT
        return usage_text
class OnlineWallpaper(OnlineOrLocalCLS):
    def __init__(self, path=None, choice=None, ngchina="no", bingchina="yes", daily_spotlight="yes", alwaysdl_bing="yes"):
        super().__init__()
        if path:
            self._path = path
        else:
            self._path = self.generate_pic_save_path()
        self._image_path = None
        self._ngchina = ngchina
        self._bingchina = bingchina
        self._daily_spotlight = daily_spotlight
        self._alwaysdl_bing = alwaysdl_bing
        self.load_config()
        if choice:
            self.choice = choice
        else:
            self.choice = self.random_choice()
    
    def generate_pic_save_path(self):
        # path = "D:\\" + os.environ.get("USERNAME") + '\\Pictures\\photo_of_the_day'
        path = os.environ.get("USERPROFILE") + '\\Pictures\\photo_of_the_day'
        # root = os.path.abspath(path)[:3]  # get the root dir of hard disk.
        # rest = os.path.abspath(path)[3:]
        #if not os.path.exists(root):
        #    path = "C:\\" + rest
        #    print("drive {} doesn't exist. \nUSE new path: {}".format(root, path))
        if not os.path.exists(path):
            os.makedirs(path)
            print("mkdir path: %s" % path)
        return path
    
    def random_choice(self):
        # generate usable list
        wallpaper_list = list()
        if self._ngchina.lower() == "yes":
            wallpaper_list.append("ngchina")
        if self._bingchina.lower() == "yes":
            wallpaper_list.append("bingchina")
        if self._daily_spotlight.lower() == "yes":
            wallpaper_list.append("daily_spotlight")
        # random select one.
        self.choice = random.choice(wallpaper_list)
        return self.choice

    def load_config(self):
        config = configparser.ConfigParser()
        config_file = self._config_file
        if os.path.exists(config_file):
            config.read(config_file)
            use_photooftheday, b, c = self.get_online_or_local(config)
            if use_photooftheday.lower() == "yes":
                photoOfTheDayCfg = config['PhotoOfTheDay'] 
                self._ngchina         = photoOfTheDayCfg['ngchina']
                self._bingchina       = photoOfTheDayCfg['bingchina']
                self._daily_spotlight = photoOfTheDayCfg['daily.spotlight']
                self._alwaysdl_bing         = photoOfTheDayCfg['alwaysdownload.bing.wallpaper']
        else:
            self.creart_def_cfg()
        self.create_usage_file()

    def getPage(self, url):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45"
        headers = { "Referer" : url, "User-Agent":user_agent }
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        return response.read().decode("utf-8")

    def download_img(self, imageUrl, image_path):
        if not os.path.exists(image_path):
            img_basename = os.path.basename(image_path)
            try:
                urllib.request.urlretrieve(imageUrl, image_path)
            except Exception as e:
                print("Download [%s] FAILED: %s" %(img_basename,e))
            else:
                print("Downloaded [%s]" % img_basename)
                self._image_path = image_path
        else:
            print("IMG exists, skip: %s" % image_path)
            self._image_path = image_path

    def run(self):
        raise NotImplementedError('Must be implemented by the subclass')

    def analyse(self):
        raise NotImplementedError('Must be implemented by the subclass')

    
    def add_water_mark(self, ori_image_file, dest_file, water_mark_text="Water Print", font_size=18, font_type="YaHei", font_color=(255, 255, 255)):
        from PIL import Image
        from PIL import ImageDraw
        from PIL import ImageFont 
        if os.path.exists(dest_file):
            return dest_file
        
        # set the font
        if font_type == "YaHei":
            font_type = "C:\\Windows\\Fonts\\Microsoft YaHei UI\\msyh.ttc"
        
        user_font_dir = 'C:\\Users\\' + os.environ.get("USERNAME") + '\\AppData\\Local\\Microsoft\\Windows\\Fonts\\'
        opposans_font = 'OPPOSans-R.ttf'
        font_dir = user_font_dir + opposans_font
        if os.path.exists(font_dir):
            # font_type = font_dir
            print(opposans_font)
        font = ImageFont.truetype(font_type, font_size)

        # open image
        img = Image.open(ori_image_file)    
        
        # Calculate the pixel size of the string
        hans_total = 0
        for s in water_mark_text:
            # There are actually many Chinese characters, but almost none of them are used. This range is sufficient
            if '\u4e00' <= s <= '\u9fef':
                hans_total += 1
        font_count = len(water_mark_text) + hans_total
        font_len = font_count * font_size // 2
        # print(font_len)
        
        # add water mark
        draw = ImageDraw.Draw(img)
        draw.text((img.width - font_len - 50, img.height - 90), water_mark_text, font_color, font=font)
        draw = ImageDraw.Draw(img)
        print("Add watermark: {}".format(water_mark_text))

        # save to target file
        img.save(dest_file)
        return dest_file


class BingChina(OnlineWallpaper):
    def __init__(self, path=None, choice=None, url='https://cn.bing.com/'):
        super().__init__(path=path, choice=choice)
        self._url = url

    # https://www.jianshu.com/p/1e4aa36ec778
    def analyse(self):
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'referer': 'https://cn.bing.com/'
        }

        r = requests.get(self._url, headers=headers)

        try:
            url = re.search(r'<div id="bgImgProgLoad" data-ultra-definition-src="(.*?)"', r.text).group(1)
            title = re.search(r'class="sc_light" title="(.*?)"', r.text).group(1)
        except AttributeError:
            print('Wrong parse rules.')
            return None

        image_url = urllib.parse.urljoin(r.url, url)
        water_mark = title
        title = title.replace('/', ' ')
        sep = '_'
        title = re.sub('\W+', sep, title)
        if title[0] == sep:
            title = title[1:]
        if title[-1] == sep:
            title = title[0:-1]
        if re.search(r"\.jpg", image_url, re.I):
            title += ".jpg"
            # WMK: watermark abbr.
        return image_url, title, water_mark
    
    def run(self):
        if self.choice != "bingchina" and self._alwaysdl_bing.lower() != "yes":
            return  "NOT bingchina"
        img_url, img_name, water_mark = self.analyse()
        print("URL:  %s" % img_url)
        prefix = img_name.split(".")[0]
        suffix = img_name.split(".")[1]
        dest_file = prefix + "-WMK." + suffix
        dest_file = os.path.join(self._path, dest_file)
        if not os.path.exists(dest_file):
            self.download_img(img_url, os.path.join(self._path,img_name))
            self.add_water_mark(self._image_path, dest_file, water_mark, font_size=18)
            os.remove(os.path.join(self._path,img_name))

        if self.choice.lower() == "bingchina" and os.path.exists(dest_file):
            self.set_wallpaper(dest_file)
        else:
            print("***** JUST download the picture without setting the wallpaper. *****\n")


class NgChina(OnlineWallpaper):
    def __init__(self, path=None, choice=None, url = u'http://www.ngchina.com.cn/photography/photo_of_the_day/'):
        super().__init__(path=path, choice=choice)
        self._url = url

    def analyse(self):
        url_content = self.getPage(self._url)
        html_suffix = re.search(r'\"/photography/photo_of_the_day/([0-9].+\.html)" title="每日一图：', url_content).group(1)
        photo_of_the_day = self._url + html_suffix
        print("photo_of_the_day:  %s" % photo_of_the_day)
        url_content = self.getPage(photo_of_the_day)
        try:
            item = re.search(r"<img src=\"http://[^>]+\"/>", url_content).group()
            img_url = re.search(r"\"(.+)\"", item).group(1)      
            title = re.search(r"<p class=\"tab_desc\">(.+)</p>", url_content).group(1)
        except Exception as e:
            print(e)
        else:
            if re.search(r"\.jpg", img_url, re.I):
                title += ".jpg"
            img_name = title
        return img_url, img_name
    
    def run(self):
        if self.choice != "ngchina":
            return  "NOT ngchina"     
        img_url, img_name = self.analyse()
        water_mark = img_name
        print("URL:  %s" % img_url)
        prefix = img_name.split(".")[0]
        suffix = img_name.split(".")[1]
        water_mark = prefix
        dest_file = prefix + "-WMK." + suffix
        dest_file = os.path.join(self._path, dest_file)
        if not os.path.exists(dest_file):
            self.download_img(img_url, os.path.join(self._path,img_name))
            self.add_water_mark(self._image_path, dest_file, water_mark, font_size=18)
            os.remove(os.path.join(self._path,img_name))
        if os.path.exists(dest_file):
            self.set_wallpaper(dest_file)


class DailySpotlight(OnlineWallpaper):
    def __init__(self, path=None, choice=None, local_path=None):
        super().__init__(path=path, choice=choice)
        if not local_path:
            local_path = self.generate_dailyspotlight_local_path()
            if os.path.exists(local_path):
                self._local_path = local_path
            else:
                raise Exception("dailyspotlight_local_path doesn't exist.")

    def generate_dailyspotlight_local_path(self):
        local_path_cmb = os.environ.get("LOCALAPPDATA") + '\\Packages\\'
        files = os.listdir(local_path_cmb)
        ContentDeliveryManager = None
        for i in files:
            if re.search(r'Microsoft\.Windows\.ContentDeliveryManager', i):
                ContentDeliveryManager = i
        if ContentDeliveryManager:        
            local_path_cmb += ContentDeliveryManager
            local_path_cmb += '\\LocalState\\Assets'
            return local_path_cmb
        else:
            print("You have not enabled DailySpotlight in Windows10 Settings.")
            return None

    def analyse(self):
        files = os.listdir(self._local_path)
        file_list = list()
        phone_file_list = list()
        for file in files:
            fi_d = os.path.join(self._local_path, file)
            if (os.path.getsize(fi_d)//1024 > 100):
                #  and imghdr.what(fi_d) != "png"
                img_pillow = Image.open(fi_d)
                if img_pillow.width > (img_pillow.height + 500):
                    file_list.append(fi_d)
                else:
                    phone_file_list.append(fi_d)       
        file_list.sort(key=lambda x:os.path.getctime(x))
        phone_file_list.sort(key=lambda x:os.path.getctime(x))
        src_file = file_list[-1]
        phone_src_file = phone_file_list[-1]
        # new file name.
        file_times_created = os.path.getctime(src_file)
        phone_file_times_created = os.path.getctime(phone_src_file)
        dest_file = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(file_times_created))
        phone_dest_file = time.strftime('%Y-%m-%d_%H-%M-%S-phone', time.localtime(phone_file_times_created))
        dest_file = os.path.join(self._path, dest_file + "." + imghdr.what(src_file))
        phone_dest_file = os.path.join(self._path, phone_dest_file + "." + imghdr.what(phone_src_file))
        # print("DailySpotlight: %s" % dest_file)
        if not os.path.exists(dest_file):
            shutil.copy(src_file, dest_file)
        if not os.path.exists(phone_dest_file):
            shutil.copy(phone_src_file, phone_dest_file)
        return dest_file

    def run(self):
        if self.choice != "daily_spotlight":
            return  "NOT daily_spotlight"
        image_path = self.analyse()
        if image_path:
            self.set_wallpaper(image_path)



# LOCAL IMAGE SETTER
class WallpaperSetter(OnlineOrLocalCLS):
    def __init__(self, img_dir):
        super().__init__()
        self._img_dir = img_dir
        self._is_newtest = None
        self._mtime_str = "NOW"
        self._scan = None # force, yes, no
        self._copy_folder = None
        self._want2copy = None # want2copy = yes, no

    @staticmethod
    def size_format(size):
        if size < 1000:
            return '%i' % size + 'size'
        elif 1000 <= size < 1000000:
            return '%.1f' % float(size/1000) + 'KB'
        elif 1000000 <= size < 1000000000:
            return '%.1f' % float(size/1000000) + 'MB'
        elif 1000000000 <= size < 1000000000000:
            return '%.1f' % float(size/1000000000) + 'GB'
        elif 1000000000000 <= size:
            return '%.1f' % float(size/1000000000000) + 'TB'

    def check_folder_mtime(self, path, mark_file):
    # Determine whether the folder is up to date
        self._is_newtest = True
        if not os.path.exists(mark_file):
            self._is_newtest = False
            self._scan = "yes"
        mtime = int(os.path.getmtime(path))
        time_tuple = time.localtime(mtime) 
        time_format = '%Y-%m-%d %H:%M:%S'
        mtime_str = time.strftime(time_format, time_tuple)
        
        if self._scan.lower() == "force":
            print("force to update. mtime[{}]".format(mtime_str))
            self._is_newtest = False
        
        if self._mtime != "None":
            time_tuple = time.strptime(self._mtime, time_format)
            mtime_int = int(time.mktime(time_tuple))
            if mtime > mtime_int:
                self._is_newtest = False
        else:
            self._is_newtest = False
        if not self._is_newtest:
            self._mtime_str = mtime_str


    # Filter images that meet the conditions
    def images_filter(self, path):
        img_list_txt = os.path.join(path, '_img_list.txt')
        self.check_folder_mtime(path, img_list_txt)
        img_list = list()
        if not self._is_newtest and self._scan.lower()!="no":
            img_list = list()
            for root, dirnames, files in os.walk(path):
                for name in files:
                    realpath = os.path.join(root, name)
                    name_t = name.lower()
                    # MUST BE a image file
                    if name_t.endswith(".jpg") or name_t.endswith(".jpeg") or name_t.endswith(".png"):
                        # image file MUST BE larger than 100KB
                        if os.path.getsize(realpath)//1024>100:
                            img_pillow = Image.open(realpath)
                            if img_pillow.width > 1900:
                                if img_pillow.width/img_pillow.height > 1.4:
                                    img_list.append(realpath)
                            img_pillow.close()                            
            self.list_converter(img_list, "to", img_list_txt)
        else:   
            img_list = self.list_converter(list(), "from", img_list_txt)
        self.update_element_in_config("WallpaperSetter", "mtime", self._mtime_str, not self._is_newtest)
        if not img_list:
            print(">>> Warning: There is no image meet the requirements in the path:\n\t{}\n"
            ">>> Consider change the path.".format(self._img_dir))
        return img_list


    def run(self):  
        self.load_config(img_dir=self._img_dir)
        if self._use_local_images.lower() != "yes":
            print("I know you don't want to use this feature.")
            return "I know."
        if not os.path.exists(self._img_dir):
            import errno
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self._img_dir)
        wallpaper_list = self.images_filter(self._img_dir)
        if wallpaper_list:
            img_file = random.choice(wallpaper_list)
            if os.path.exists(img_file):
                self.set_wallpaper(img_file)
                self.update_element_in_config("WallpaperSetter", "wallpaper", img_file, True)  
            

    def load_config(self, img_dir="MUSTDEFINED", copy_folder="None", 
            scan="yes", want2copy='no', use_wallpapersetter="yes", last_img_dir="None"):
        config = configparser.ConfigParser()
        config_file = self._config_file
        mtime = "None"
        if os.path.exists(config_file):
            config.read(config_file)
            a, use_wallpapersetter,c = self.get_online_or_local(config)
            if use_wallpapersetter.lower() == "yes":
                wallpaperSetterCfg = config['WallpaperSetter']
                img_dir = wallpaperSetterCfg['img_dir']
                mtime = wallpaperSetterCfg['mtime']
                last_img_dir = wallpaperSetterCfg['last_img_dir']
                scan = wallpaperSetterCfg['scan']
                copy_folder = wallpaperSetterCfg['copy_folder']
                want2copy = wallpaperSetterCfg['want2copy']
            if img_dir != last_img_dir:
                print("last_img_dir: {}".format(last_img_dir))
                self.update_element_in_config("WallpaperSetter", "last_img_dir", img_dir, True)         
        else:
            self.creart_def_cfg()
        
        self.create_usage_file()
        self._use_local_images = use_wallpapersetter
        self._img_dir = img_dir
        self._copy_folder = copy_folder
        self._mtime = mtime
        self._scan = scan
        self._want2copy = want2copy
    
    def list_converter(self, list_=list(), action="from", list_file="list.txt"):
        if action.lower() == "from":
            list_ = list()
            with open(list_file, 'r', encoding="utf-8") as f:
                list_str = f.readlines()
                for item in list_str:
                    item = item.strip('\n')
                    if item:
                        item = item.split(' //', 1)[0]
                        item = item.split(' //', 1)[0]
                        list_.append(item)
            return list_
        elif action.lower() == "to":
            with open(list_file, 'w', encoding="utf-8") as f:
                for i in list_:
                        f.write(i + '\n')
            return None
        else:
            raise Exception("No such action[{}]".format(action))

    def copyto(self, dest_dir=None):
        if self._want2copy.lower() != "yes":
            return "completed"
        self.load_config(img_dir=self._img_dir)
        if not os.path.exists(self._img_dir):
            import errno
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self._img_dir)   
        if self._copy_folder != "None":
            dest_dir=self._copy_folder            
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        files_list = self.images_filter(self._img_dir)
        index = 0
        exists_list = list()
        exists_list_txt = os.path.join(dest_dir, "_existing_file_list.txt")
        for file in files_list:
            index += 1
            basename = os.path.basename(file)
            dest_file = os.path.join(dest_dir, basename)
            
            if os.path.exists(dest_file):
                if not os.path.exists(exists_list_txt):
                    exists_list.append(file)
            
            if not os.path.exists(dest_file):
                shutil.copy(file, dest_file)
                print("[{:>02d}]: copied [ {} ]".format(index, dest_file))
        index = 0
        if exists_list:
            for file in exists_list:
                index += 1
                print("[{:>02d}]: existed [ {} ]".format(index, file))
            exists_list.append('^^^ Some file have been named repeatedly. TIME[{}]. ^^^'.format(time.asctime(time.localtime(time.time()))))
            self.list_converter(exists_list, "to", exists_list_txt)
            print("\n^^^ Some file have been named repeatedly. ^^^")
        print("Copy completed.")
    

def configparser_sample():
    conf = configparser.ConfigParser()
    conf.read("config.ini")
    
    # get section,option value
    name = conf.get("section1", "name")
    age = conf.get("section1", "age")

    #get all the sections
    sections = conf.sections()

    print(name, age, sections)
    
    # update section, option value
    conf.set("section2", "port", "8081")
    # write to section, add new option value
    conf.set("section2", "IEPort", "80")
    
    # add new section
    conf.add_section("new_section")
    conf.set("new_section", "new_option", "http://www.cnblogs.com/tankxiao")  
    # save to config file.
    conf.write(open("c:\\test.conf","w"))



def online_setter():   
    online_wallpaper = OnlineWallpaper()
    ch = online_wallpaper.choice
    print(">>> the choice is: {}.".format(ch))   
    bingchina = BingChina(choice=ch)
    ngchina = NgChina(choice=ch)
    dailyspotlight = DailySpotlight(choice=ch)
    bingchina.run()
    ngchina.run()
    dailyspotlight.run()
    
def local_setter():
    wallpaper_setter = WallpaperSetter(img_dir="D:\jared\erotic\[Wanimal-Wallpaper]")
    print("Starting.")
    try:
        wallpaper_setter.run()
        wallpaper_setter.copyto(dest_dir="C:\\Users\\jared\\Pictures")
    except Exception as e:
        import traceback
        print("{0}\n{1}".format(str(e), traceback.format_exc()))
    else:
        print("Finished.")  

class ConfigParserReader(PyinstallerPath):
    def __init__(self, config_file=None):
        super().__init__()
        if config_file:
            self._config_file = config_file
        else:
            self._config_file = os.path.join(self._getcwd, "config.ini")

    def load_config(self):
        config = configparser.ConfigParser()
        config_file = self._config_file
        if os.path.exists(config_file):
            config.read(config_file)
            onlinelocalCfg = config['OnlineOrLocal']
            use_photooftheday = onlinelocalCfg['use_photooftheday']
            use_wallpapersetter = onlinelocalCfg['use_wallpapersetter']
            if use_wallpapersetter.lower() == "yes":
                return "use_wallpapersetter"
            elif use_photooftheday.lower() == "yes":
                return "use_photooftheday"                
            else:
                return "DoNothing."
        else:
            return "NoConfig.ini"
            

if __name__ == "__main__":
    cfg = ConfigParserReader()
    ret = cfg.load_config()
    if ret == "use_photooftheday":
        online_setter()
    elif ret == "use_wallpapersetter":
        local_setter()
    else:
        online_setter()