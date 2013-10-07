import os
import sys
import datetime
import time
import urllib.request, urllib.error, urllib.parse
import xml.etree.ElementTree as ET

if len(sys.argv) != 3:
    print("Usage: chinesepod_downloader.py <feed_url> <output_dir>")
    sys.exit(1)

feed_src = sys.argv[1]
feed = ET.fromstring(urllib.request.urlopen(feed_src).read())
output_dir = sys.argv[2]
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
    output.write(urllib.request.urlopen(remote_uri).read())
    output.close()

if __name__ == "__main__":
    podcasts = feed.findall(".//item")
    items = 0
    for podcast in podcasts:
        title = podcast.find("title").text.strip()
        uri = podcast.find("enclosure").attrib["url"]
        date = podcast.find("pubDate").text
        lesson_type = uri[uri.rindex("."):]

        folder_name = "%s - %s" % (time.strftime("%Y-%m-%d", date_for(date)), folder_for(title))
        base_path = os.path.join(output_dir, folder_name)
        file_path = os.path.join(base_path, folder_name + lesson_type)

        if os.path.exists(base_path):
            if os.path.exists(file_path):
                print(("Skipping found lesson [%s%s]" % (path, lesson_type)))
                continue
        else:
            os.mkdir(base_path)

        print(("Downloading lesson [%s%s]" % (folder_name, lesson_type)))
        download(uri, file_path)
        items += 1

        time.sleep(.5)
    print("Finished! Downloaded %d items." % items)


