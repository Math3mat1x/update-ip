#!/usr/bin/python3
import time
import json
import requests
import os.path as path

ip = requests.get("https://ifconfig.me/").text
file = path.join(path.abspath(path.dirname(__file__)), "ip.json")
url = "https://dynamicdns.park-your-domain.com/update"

with open(file, "r") as f:
    ips = f.read()

if ips:
    ips = json.loads(ips)
else:
    ips = [(None,None,None)]

def update(domain, password, ip, hosts=["@"]):
    data = {
            "domain": domain,
            "password": password,
            "ip": ip
            }

    for host in hosts:
        data["host"] = host
        tmp = data.copy()
        del(tmp["password"])
        print(tmp) # see progress
        try:
            r = requests.get(url, data)
            if r.status_code != 200:
                raise Exception
        except:
            with open(path.join(path.abspath(path.dirname(__file__)), "error.log"), "a") as f:
                f.write("ERROR on {}".format(time.time()))

    return True # success


def main(domain, password, hosts=["@"]):
    if ips[-1][0] != ip:
        update(domain, password, ip, hosts=hosts)
        if not ips[0][0]:
            del ips[0]
        ips.append((ip, time.time()))
        with open("ip.json", "w") as f:
            f.write(json.dumps(ips))

from config import config

for row in config:
    domain = row[0]
    password = row[1]
    hosts = row[2]

    main(domain, password, hosts)
