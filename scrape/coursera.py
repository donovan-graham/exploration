from celery.task import task
import math
import re
import requests
from bs4 import BeautifulSoup
import urllib
import os.path
import urllib2

url = "https://class.coursera.org/algo-004/lecture/index"
video_re = re.compile("^Video*")



def downloadChunks(url):
    """Helper to download large files
        the only arg is a url
       this file will go to a temp directory
       the file will also be downloaded
       in chunks and print out how much remains
    """

    temp_path = "/tmp/"
    try:

        req = urllib2.urlopen(url)
        total_size = int(req.info().getheader('Content-Length').strip())
        downloaded = 0
        CHUNK = 256 * 10240
        with open(file, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                print math.floor( (downloaded / total_size) * 100 )
                if not chunk: break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        print "HTTP Error:",e.code , url
        return False
    except urllib2.URLError, e:
        print "URL Error:",e.reason , url
        return False

    return file

def slugify(value):
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\d\s\.\-\[\]\(\)]', '', value).strip())
    return value

@task
def downloader(download_url, save_path):
    base_path = "/var/www/webapp/media/alogrithms/"

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    if not os.path.isfile(save_path):
        print "downloading ... %s" % download_url
        urllib.urlretrieve(download_url, "%s%s" % (base_path, save_path))
        print "... completed"



course = {}
r = requests.get(url)
cnt = 1
if r.status_code == requests.codes.ok:
    soup = BeautifulSoup(r.text)

    course = soup.find("h1", class_="hidden")
    if course:
        print course.get_text(strip=True)


    for li in soup.find_all("li"):
        lecture = li.find('a', class_="lecture-link")
        if lecture:

            pdf = li.find('a', title="PDF")
            if pdf:
                pdf = pdf.get('href')
                # file_name = "%03d.pdf" %(cnt)
                file_name = slugify("%03d. %s.pdf" %(cnt, lecture.get_text(strip=True)))
                downloader(pdf, file_name)

            video = li.find('a', title=video_re)
            if video:
                video = video.get('href')
                file_name = slugify("%03d. %s.mp4" %(cnt, lecture.get_text(strip=True)))
                downloader(video, file_name)


            course[cnt] = {
                    'name': "%03d. %s" %(cnt, lecture.get_text(strip=True)),
                    'pdf': pdf,
                    'video': video
                }

            cnt += 1
else:
    print "oops"

