import getpass
import readline

import netifaces as ni
import requests


def get_ip(interface="wlan0"):
    ip4 = ni.ifaddresses(interface)[ni.AF_INET][0]["addr"]
    ip6 = ni.ifaddresses(interface)[ni.AF_INET6][0]["addr"]
    return ip4, ip6


def login(username, password, ip, url):
    ip4, ip6 = ip
    data = {
        "username": username,
        "password": password,
        "mac": "",
        "ipv4": ip4,
        "ipv6": ip6,
        "loginType": "manual",
        "loginMethod": "ldap",
        "hash": "",
        "hashc": "",
        "submit": "Log In",
    }

    res = requests.post(url, data=data)
    url = res.url
    return url


def save_user():
    with open("user.txt", "w") as f:
        user = input("Enter your username: ")
        pwd = getpass.getpass(prompt="Enter your password: ")
        f.write(f"{user}\n{pwd}")

    return user, pwd


def read_user():
    with open("user.txt", "r") as f:
        lines = f.readlines()
        if not lines:
            user, pwd = save_user()
        else:
            user, pwd = [line.strip() for line in lines]

    return user, pwd


def main():

    while True:
        try:
            user, pwd = read_user()
            url = "https://login1.ku.ac.th/index.jsp?action=login"
            ip4, ip6 = get_ip("wlan0")

            res = login(user, pwd, (ip4, ip6), url)

            if "info" in res:
                print("Login success")
                break
            elif "error=3" in res:
                raise Exception("ip")
            else:
                raise Exception("credential")

        except Exception as e:
            msg = e.args[0]
            if msg == "credential":
                print("invalid username or password.")
                save_user()
            elif msg == "ip":
                print("already login ( https://info.ku.ac.th ) or ip already exists.")
                break
        except:
            print("I don't know anymore. :< ")
            return


if __name__ == "__main__":
    main()
