# -*- coding: UTF-8 -*-
import urllib.request
import requests
import re
import os
import ctypes
import time
import random

class WallpaperSetter():
    def __init__(self, path):
        self._path = path
        self._image_path = None

    def getPage(self, url):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45"
        headers = { "Referer" : url, "User-Agent":user_agent }
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        return response.read().decode("utf-8")

    def download_img(self, imageUrl, path, img_name):
        dir(img_name)
        image_path = path + u"/" + img_name
        if not os.path.exists(image_path):
            img_basename = os.path.basename(image_path)
            try:
                urllib.request.urlretrieve(imageUrl, image_path)
            except Exception as e:
                print("Download[%s] FAILED: %s" %(img_basename,e))
            else:
                print("SUCCEED![%s]" % img_basename)
                self._image_path = image_path
        else:
            print("SUCCEED! IMG exists,skip: %s" % image_path)
            self._image_path = image_path
    @staticmethod
    def set_wallpaper(pic_path):
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDWININICHANGE = 0x02
        ret = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, pic_path, \
                                                   SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
        if (ret == 0):
            ret = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, pic_path, \
                                                   SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
        if (ret == 1):
            print("set wallpaper succeed!!!")
        else:
            print("set wallpaper failed!!! Try twice!")

    def run(self):
        img_url, img_name = self.analyse()
        print("img_url:  %s" % img_url)
        self.download_img(img_url, self._path, img_name)
        if self._image_path:
            self.set_wallpaper(self._image_path)

    def analyse(self):
        raise NotImplementedError('Must be implemented by the subclass')


class BingChina(WallpaperSetter):
    def __init__(self, path = u'C:\\Users\\jared\\Pictures\\photo_of_the_day',
                 url = 'https://cn.bing.com/'):
        super().__init__(path)
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
            return

        image_url = urllib.parse.urljoin(r.url, url)
        title = title.replace('/', ' ')
        sep = '_'
        title = re.sub('\W+', sep, title)
        if title[0] == sep:
            title = title[1:]
        if title[-1] == sep:
            title = title[0:-1]
        if re.search(r"\.jpg", image_url, re.I):
            title += ".jpg"
        return image_url, title


class NgChina(WallpaperSetter):
    def __init__(self, path = u'C:\\Users\\jared\\Pictures\\photo_of_the_day',
                 url = u'http://www.ngchina.com.cn/photography/photo_of_the_day/'):
        super().__init__(path)
        self._url = url

    def analyse(self):
        url_content = self.getPage(self._url)
        html_suffix = re.search(r'\"/photography/photo_of_the_day/([0-9].+\.html)" title="每日一图：', url_content).group(1)
        photo_of_the_day = self._url + html_suffix
        print("photo_of_the_day:  %s" % photo_of_the_day)
        url_content = self.getPage(photo_of_the_day)
        item = re.search(r"<img src=\"http://[^>]+\" />", url_content).group()
        img_url = re.search(r"\"(.+)\"", item).group(1)
        try:
            title = re.search(r"<p class=\"tab_desc\">(.+)</p>", url_content).group(1)
        except Exception as e:
            img_name = img_url.split('/')[-1]
        else:
            if re.search(r"\.jpg", img_url, re.I):
                title += ".jpg"
            img_name = title

        return img_url, img_name


if __name__ == "__main__":
    path = u"C:\\Users\\jared\\Pictures\\photo_of_the_day"
    if random.randint(0,1) == 0:
        wallpaper_setter = NgChina(path = path)
    else:
        wallpaper_setter = BingChina(path = path)
    wallpaper_setter.run()


