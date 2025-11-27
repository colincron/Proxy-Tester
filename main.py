import os.path, ipaddress
from urllib.request import urlretrieve
import requests
import urllib3.exceptions

test_http_site = 'http://httpforever.com'
test_https_site = 'https://docs.python.org/3/library/ipaddress.html'

def proxy_test(ip_address, port, type):
    ipa = ipaddress.ip_address(ip_address)
    str(ipa)
    host_up = os.system(f"ping -c 1 -q {ipa} > /dev/null") == 0
    if host_up:
        print("[-] " + str(ipa) + " seems to be up. Determining if it's a functioning proxy.\n")
        ip_port_str = str(ipa) + ":" + str(port)
        proxies = {
            type: type+"://"+ip_port_str,
            }
        try:
            if type == "https":
                response = requests.get(test_https_site, proxies=proxies)
            elif type == "http":
                response = requests.get(test_http_site, proxies=proxies)

            if response.status_code == 200:
                full_string = type+"://" + str(ipa) + ":" + str(port)
                print("[+] This one works: " + full_string)
                file_writer(full_string, "http")
            else:
                print("[-] This one doesn't "+ "http://" + ip_address + ":" + str(port) )
        except ConnectionResetError:
            print("[-] Connection reset by peer. Connection Reset Error")
        except TimeoutError:
            print("[-] TimeoutError")
        except urllib3.exceptions.MaxRetryError:
            print("[-] Max retries. MaxRetryError")
        except requests.exceptions.ProxyError:
            print("[-] Max retries exceeded. requests.exceptions.ProxyError")
        except requests.exceptions.TooManyRedirects:
            print("[-] Too many redirects. requests.exceptions.TooManyRedirects")
        except requests.exceptions.ConnectionError:
            print("[-] Connection aborted - Remote end closed connection without response")
        except urllib3.exceptions.ReadTimeoutError:
            print("[-] ReadTimeoutError")
    else:
        print("[-] " + str(ipa) + " seems to be down\n")

def file_handler(type):
    if type.lower() == "http":
        url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/http/data.txt"
    elif type.lower() == "https":
        url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/https/data.txt"

    if os.path.isfile(type + '_data.txt'):
        print(type + "_data.txt already exists")

    else:
        print("downloading " + type + "_data.txt proxy list")
        urlretrieve(url, type + '_data.txt')
    with open(type + '_data.txt') as lines:
        if type == "http":
            for line in lines:
                ip = line.replace("http://","").split(":")[0]
                port = line.replace("http://","").split(":")[1]
                proxy_test(ip, port, type)
        elif type == "https":
            for line in lines:
                ip = line.replace("https://","").split(":")[0]
                port = line.replace("https://","").split(":")[1]
                proxy_test(ip, port, type)

def file_writer(full_string, type):
    f = open(type + "_proxies.txt", "a")
    f.write(full_string)
    f.close()

if __name__ == "__main__":
    user_input = str(input("Are you testing http or https today? "))
    if user_input.lower() == "http":
        file_handler("http")
    elif user_input.lower() == "https":
        file_handler("https")