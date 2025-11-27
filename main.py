import os.path
from urllib.request import urlretrieve
import requests
import urllib3.exceptions

# Initial Commit

test_http_site = 'http://httpforever.com'

def get_file():
    url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/http/data.txt"
    if os.path.isfile('data.txt'):
        print("data.txt already exists")
        return
    else:
        print("downloading data.txt proxy list")
        urlretrieve(url, 'data.txt')

def http_proxy_test(ip_address, port):
    ip_port_str = ip_address + ":" + str(port)
    proxies = {
        'http': ip_port_str,
        }
    try:
        response = requests.get(test_http_site, proxies=proxies)
        if response.status_code == 200:
            full_string = "http://" + ip_address + ":" + str(port)
            print("[+] This one works: " + full_string)
            f = open("proxies.txt", "a")
            f.write(full_string)
            f.close()

        else:
            print("[-] This one doesn't "+ "http://" + ip_address + ":" + str(port) )
    except ConnectionResetError:
        print("[-] Connection reset by peer. Connection Reset Error")
    except urllib3.exceptions.MaxRetryError:
        print("[-] Max retries. MaxRetryError")
    except requests.exceptions.ProxyError:
        print("[-] Max retries exceeded. requests.exceptions.ProxyError")
    except requests.exceptions.TooManyRedirects:
        print("[-] Too many redirects. requests.exceptions.TooManyRedirects")


def file_handler():
    get_file()
    with open('data.txt') as lines:
        for line in lines:
            ip = line.replace("http://","").split(":")[0]
            port = line.replace("http://","").split(":")[1]
            http_proxy_test(ip, port)

file_handler()