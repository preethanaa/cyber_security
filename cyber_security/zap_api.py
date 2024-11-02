import requests
import time

import os

# Disable any global proxy settings
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''


#ZAP_URL = "http://localhost:3000"
ZAP_URL = "http://127.0.0.1:8080"
API_KEY = "16vhrldd6dptdqtu04pqg3d6" #your-zap-api-key  Set this in ZAP under Tools -> Options -> API

# Start the spidering process to discover pages
def start_spider(target_url):
    print(f"[*] Starting spider for {target_url}")
    spider_url = f"{ZAP_URL}/JSON/spider/action/scan/"
    params = {
        "apikey": API_KEY,
        "url": target_url,
        "maxChildren": 10
    }
    response = requests.get(spider_url, params=params)
    scan_id = response.json().get("scan")
    return scan_id

# Check spider status
def get_spider_status(scan_id):
    status_url = f"{ZAP_URL}/JSON/spider/view/status/"
    params = {"apikey": API_KEY, "scanId": scan_id}
    status_response = requests.get(status_url, params=params)
    return status_response.json().get("status")

# Start active scan
def start_active_scan(target_url):
    print(f"[*] Starting active scan for {target_url}")
    scan_url = f"{ZAP_URL}/JSON/ascan/action/scan/"
    params = {
        "apikey": API_KEY,
        "url": target_url,
    }
    response = requests.get(scan_url, params=params)
    scan_id = response.json().get("scan")
    return scan_id

# Check active scan status
def get_active_scan_status(scan_id):
    status_url = f"{ZAP_URL}/JSON/ascan/view/status/"
    params = {"apikey": API_KEY, "scanId": scan_id}
    status_response = requests.get(status_url, params=params)
    return status_response.json().get("status")

# Retrieve scan results
def get_scan_results():
    results_url = f"{ZAP_URL}/JSON/core/view/alerts/"
    params = {"apikey": API_KEY}
    response = requests.get(results_url, params=params)
    return response.json()

# Main scan function
def run_scan(target_url):
    spider_id = start_spider(target_url)

    while int(get_spider_status(spider_id)) < 100:
        print("[*] Spidering in progress...")
        time.sleep(5)

    print("[+] Spidering completed.")

    scan_id = start_active_scan(target_url)

    while int(get_active_scan_status(scan_id)) < 100:
        print("[*] Active scan in progress...")
        time.sleep(5)

    print("[+] Active scan completed.")
    return get_scan_results()

# Example usage
#target_url = "http://example.com"
#target_url = "http://juice-shop.herokuapp.com"
target_url = "https://www.godigit.com/"
scan_results = run_scan(target_url)
print(scan_results)