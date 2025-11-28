import os.path, ipaddress, requests, urllib3.exceptions
from urllib.request import urlretrieve

test_site = 'http://httpforever.com'

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
            response = requests.get(test_site, proxies=proxies)

            if response.status_code == 200:
                full_string = type+"://" + str(ipa) + ":" + str(port)
                print("[+] This one works: " + full_string)
                file_writer(full_string, type)
            else:
                print("[-] This one doesn't "+ type +"://" + ip_address + ":" + str(port) )

        except ConnectionResetError:
            print("[-] Connection reset by peer. Connection Reset Error\n")
        except TimeoutError:
            print("[-] TimeoutError\n")
        except urllib3.exceptions.MaxRetryError:
            print("[-] Max retries. MaxRetryError\n")
        except requests.exceptions.ProxyError:
            print("[-] Max retries exceeded. requests.exceptions.ProxyError\n")
        except requests.exceptions.TooManyRedirects:
            print("[-] Too many redirects. requests.exceptions.TooManyRedirects\n")
        except requests.exceptions.ConnectionError:
            print("[-] Connection aborted - Remote end closed connection without response\n")
        except urllib3.exceptions.ReadTimeoutError:
            print("[-] ReadTimeoutError\n")
    else:
        print("[-] " + str(ipa) + " seems to be down\n")

def file_handler(type):
    url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/"+type+"/data.txt"

    if os.path.isfile(type + '_data.txt'):
        print(type + "_data.txt already exists\n")
    else:
        print("downloading " + type + "_data.txt proxy list\n")
        urlretrieve(url, type + '_data.txt')
    with open(type + '_data.txt') as lines:
        if type != "https":
            for line in lines:
                ip = line.replace(type + "://","").split(":")[0]
                port = line.replace(type + "://","").split(":")[1]
                proxy_test(ip, port, type)
        elif type == "https":
            for line in lines:
                if line.startswith("https:"):
                    ip = line.replace(type + "://", "").split(":")[0]
                    port = line.replace(type + "://", "").split(":")[1]
                    proxy_test(ip, port, type)
                elif line.startswith("http:"):
                    ip = line.replace("http://", "").split(":")[0]
                    port = line.replace("http://", "").split(":")[1]
                    proxy_test(ip, port, type)


def file_writer(full_string, type):
    f = open(type + "_proxies.txt", "a")
    f.write(full_string)
    f.close()

if __name__ == "__main__":
    user_input = str(input("Are you testing http, https, socks4, or socks5 today? "))
    if user_input.lower() == "http":
        file_handler("http")
    elif user_input.lower() == "https":
        file_handler("https")
    elif user_input.lower() == "socks4":
        file_handler("socks4")
    elif user_input.lower() == "socks5":
        file_handler("socks5")