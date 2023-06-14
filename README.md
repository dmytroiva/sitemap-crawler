# sitemap-crawler

## A script that will crawl any sitemap.xml file for your site.
Details of the script:

- go through all the links from the sitemap.xml file (and its subfiles) and check that the pages are available and return a 200 response;
- the passage is done in single-threaded mode. Allows you to reduce the load on the server and prevent server spam;
- the script is suitable for checking any sitemap.xml, just enter the domain name;
- progress changes dynamically: 'Processing https://your-sitemap.xml... Done. Success - 477. Failed - 3. (12.44%)' change % in real-time, without using the tqdm library;
- saves the test results in 2 files: Successful (only status 200) and unsuccessful (other statuses).

### A little demo video:
![sitemap_demo](https://github.com/dmytroiva/sitemap-crawler/blob/dev/media/sitemap_demo.gif)

  
This will allow Nginx to cache these pages when they are accessed and then give them to users and search engines faster.
To start script use command:
> python3 path/to/the/script/sitemap_crawler_v5.py www.gymshark.com

## To compile script for **Linux OS**, use **pyinstaller**:

> run [pyinstaller](https://pyinstaller.org/en/stable/installation.html "to install hit the link") --onefile **sitemap_crawler_v5.py**

## If your script didn't start at other OS try another example to compile into Python executable file:

 `pyinstaller --onefile --add-binary "/usr/bin/python3:." --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0:." --add-data "/usr/lib/python3/dist-packages/requests:requests" --add-binary "/home/vorting/.local/lib/python3.11/site-packages:." sitemap_crawler_v5.py`

All rights reserved by Dmytro (Vorting) Ivanov
