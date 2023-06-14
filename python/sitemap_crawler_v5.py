from xml.etree.ElementTree import fromstring
import requests
import sys

# To run this script use command with specific URL parameters:
# python3 path/to/the/script/sitemap_crawler_v5.py example.com
# To compile script for Linux OS, use pyinstaller:
# run 'pyinstaller --onefile sitemap_crawler_v5.py'
# Another example to compile into pyton executable file:
# pyinstaller --onefile --add-binary "/usr/bin/python3:." --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0:." --add-data "/usr/lib/python3/dist-packages/requests:requests" --add-binary "/home/vorting/.local/lib/python3.11/site-packages:." sitemap_crawler_v5.py


def check_url_availability(url):
    try:
        response = requests.head(url)
        return response.status_code
    except requests.exceptions.RequestException:
        return -1


def get_url_from_sitemap(loc):
    return loc.text.split('/')[-1]


def crawl_sitemap(sitemap_url, parent_url=None, parent_success=0, parent_fail=0):
    try:
        response = requests.get(sitemap_url)
        root = fromstring(response.text)
        total_urls = len(root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"))
        processed_urls = 0
        success_count = 0
        fail_count = 0

        for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            url = loc.text
            response_code = check_url_availability(url)

            if response_code == 200:
                success_count += 1
                output_file = f"{domain}_success.txt"
            else:
                fail_count += 1
                output_file = f"{domain}_fail.txt"

            with open(output_file, "a") as f:
                f.write(url + "\n")
                f.write(f"Response code: {response_code}\n")

            processed_urls += 1
            progress = (processed_urls / total_urls) * 100
            sys.stdout.write(
                f"\rProcessing {sitemap_url}... Done. Success - {success_count}. Failed - {fail_count}. ({progress:.2f}%)")
            sys.stdout.flush()

        if parent_url is not None:
            print()

        # Check child sitemap URLs
        for sitemap_loc in root.findall(
                ".//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            child_sitemap_url = sitemap_loc.text
            crawl_sitemap(child_sitemap_url, parent_url=sitemap_url, parent_success=success_count,
                          parent_fail=fail_count)

    except requests.exceptions.RequestException as e:
        print("Error while getting sitemap.xml:", e)
    except BrokenPipeError:
        pass


if len(sys.argv) < 2:
    print("You should provide a domain name as a parameter.")
    sys.exit(1)

domain = sys.argv[1]

sitemap_url = "https://" + domain + "/sitemap.xml"

crawl_sitemap(sitemap_url)
