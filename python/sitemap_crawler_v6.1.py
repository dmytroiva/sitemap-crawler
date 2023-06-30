from xml.etree.ElementTree import fromstring
import requests
import sys
import os


def check_url_availability(url):
    try:
        response = requests.head(url)
        return response.status_code
    except requests.exceptions.RequestException:
        return -1


def get_sitemap_url_from_robots_txt(domain):
    robots_url = f"https://{domain}/robots.txt"
    try:
        response = requests.get(robots_url)
        lines = response.text.split("\n")
        for line in lines:
            if line.lower().startswith("sitemap:"):
                sitemap_url = line.split(":", 1)[1].strip()
                if sitemap_url.endswith(".xml"):
                    return sitemap_url
    except requests.exceptions.RequestException as e:
        print("Error while getting robots.txt:", e)

    return None


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
                output_file = f"/app/data/{domain}_success.txt"
            else:
                fail_count += 1
                output_file = f"/app/data/{domain}_fail.txt"

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


if __name__ == "__main__":
    # Read domain from domain.txt file
    domain_txt_path = "/app/data/domain.txt"

    if len(sys.argv) >= 2:
        # If a command line argument is passed, use it
        domain = sys.argv[1]
    else:
        # Read domain from domain.txt file
        with open(domain_txt_path, "r") as file:
            domain = file.read().strip()

    if not domain:
        print("Domain is not specified.")
        sys.exit(1)

    # Get sitemap URL from robots.txt
    sitemap_url = get_sitemap_url_from_robots_txt(domain)

    if sitemap_url is not None:
        # Save sitemap domain to domain.txt
        with open(domain_txt_path, "w") as file:
            file.write(domain)

        crawl_sitemap(sitemap_url)
    else:
        print("No sitemap URL found in robots.txt.")
