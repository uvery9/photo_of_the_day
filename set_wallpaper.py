import urllib.request
import requests
import re
import os
import ctypes

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

    def download_img(self, imageUrl, path, img_name = None):
        if not img_name:
            img_name = imageUrl.split('/')[-1]
        imagePath = path + "/" + img_name
        print(imagePath)
        if not os.path.exists(imagePath):
            img_basename = os.path.basename(imagePath)
            try:
                urllib.request.urlretrieve(imageUrl, imagePath)
            except Exception as e:
                print("Download[%s] FAILED: %s" %(img_basename,e))
            else:
                print("SUCCEED![%s]" % img_basename)
                self._image_path = imagePath
        else:
            print("SUCCEED! IMG exists,skip: %s" % imagePath)
    
    @staticmethod
    def set_wallpaper(pic_path):
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_UPDATEINIFILE = 0x01;
        SPIF_SENDWININICHANGE = 0x02;
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, pic_path, \
                                                   SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
        print("set wallpaper succeed!!!")

    def run(self):
        img_url, img_name = self.analyse()
        print("img_url:  %s" % img_url)
        self.download_img(img_url, self._path, img_name)
        if self._image_path:
            self.set_wallpaper(self._image_path)

    def analyse(self):
        raise NotImplementedError('Must be implemented by the subclass')


class BingChina(WallpaperSetter):
    def __init__(self, path = u'C:\\Users\\jared\\Pictures\\Bing_photo_of_the_day',
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
        if re.search(r"\.jpg", image_url):
            title += ".jpg"
        return image_url, title


class NgChina(WallpaperSetter):
    def __init__(self, path = u'C:\\Users\\jared\\Pictures\\NGC_photo_of_the_day',
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
        img_name = img_url.split('/')[-1]
        return img_url, img_name


if __name__ == "__main__":
    ngc = NgChina(path = u"C:\\Users\\jared\\Pictures\\NGC_photo_of_the_day")
    ngc.run()
    # bingChina = BingChina(path = u'C:\\Users\\jared\\Pictures\\Bing_photo_of_the_day')
    # bingChina.run()
