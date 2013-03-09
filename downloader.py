import os
import datetime
import time
import urllib2
import xml.etree.ElementTree as ET

feed_src = "http://chinesepod.com/[ENTER YOUR FEED URL]"
feed = ET.fromstring(urllib2.urlopen(feed_src).read())
# feed_src = "\path\to\your\feed.xml"
# feed = ET.parse(feed_src).getroot()

def folder_for(title):
    if title.startswith("PDF"):
        title = title[title.index("-")+2:]
    return title.replace("?", "")

def date_for(date_str):
    return time.strptime(date_str.split("-")[0], "%a, %d %b %Y %H:%M:%S ")

def download(remote_uri, local_uri):
    output = open(local_uri,"wb")
    output.write(urllib2.urlopen(remote_uri).read())
    output.close()

if __name__ == "__main__":
    podcasts = feed.findall(".//item")
    items = 0
    for podcast in podcasts:
        title = podcast.find("title").text.strip()
        uri = podcast.find("enclosure").attrib["url"]
        date = podcast.find("pubDate").text
        lesson_type = uri[uri.rindex("."):]

        path = "%s - %s" % (time.strftime("%Y-%m-%d", date_for(date)), folder_for(title))

        if os.path.exists(path):
            if os.path.exists(os.path.join(path, path + lesson_type)):
                print("Skipping found lesson [%s%s]" % (path, lesson_type))
                continue
        else:
            os.mkdir(path)

        print("Downloading lesson [%s%s]" % (path, lesson_type))
        download(uri, os.path.join(path, path + lesson_type))
        items += 1

        time.sleep(.5)
    print("Finished! Downloaded %d items." % items)


