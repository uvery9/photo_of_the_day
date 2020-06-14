import urllib.request
import re
import os
import ctypes

class NgChina:
    def __init__(self, path = u"C:\\Users\\jared\\Pictures\\NGC_photo_of_the_day"):
        self._path = path
        self.image_path = None

    def analyze_ngc(self):
        url = u'http://www.ngchina.com.cn/photography/photo_of_the_day/'
        url_content = self.getPage(url)
        html_suffix = re.search(r'\"/photography/photo_of_the_day/([0-9].+\.html)" title="每日一图：', url_content).group(1)
        photo_of_the_day = url + html_suffix
        print("photo_of_the_day:  %s" % photo_of_the_day)
        url_content = self.getPage(photo_of_the_day)
        item = re.search(r"<img src=\"http://[^>]+\" />", url_content).group()
        jpg_url = re.search(r"\"(.+)\"", item).group(1)
        return jpg_url

    def getPage(self, url):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
        headers = { "Referer" : url, "User-Agent":user_agent }
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        return response.read().decode("utf-8")

    def download_img(self, imageUrl, path):
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
                self.image_path = imagePath
        else:
            print("SUCCEED! IMG exists,skip: %s" % imagePath)
    def run(self):
        jpg_url = self.analyze_ngc()
        print("jpg:  %s" % jpg_url)
        self.download_img(jpg_url, self._path)
        if self.image_path:
            self.set_wallpaper(self.image_path)

    @staticmethod
    def set_wallpaper(pic_path):
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_UPDATEINIFILE = 0x01;
        SPIF_SENDWININICHANGE = 0x02;
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, pic_path, \
                                                   SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
        print("set wallpaper succeed!!!")

if __name__ == "__main__":
    ngc = NgChina(path= u"C:\\Users\\jared\\Pictures\\NGC_photo_of_the_day")
    ngc.run()
