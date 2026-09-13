import requests

API_KEY = "YOUR_API_KEY"

cache = {}

def check_ip(ip):

    if ip in cache:
        return cache[ip]

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    headers = {"x-apikey": API_KEY}

    try:
        res = requests.get(url, headers=headers, timeout=5)

        if res.status_code == 200:

            data = res.json()
            stats = data["data"]["attributes"]["last_analysis_stats"]

            if stats["malicious"] > 0:
                result = "MALICIOUS"
            else:
                result = "SAFE"
        else:
            result = "UNKNOWN"

    except:
        result = "ERROR"

    cache[ip] = result
    return result