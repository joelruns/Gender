#!/usr/bin/python
import requests
import time
import math
import sys

gen = sys.argv[1]
with open("meta/" + gen + ".out", "r") as f:
    urls = []
    for line in f:
        k ="https://okcupid.com/profile/"+line.strip('\n')
        urls.append(k)
        with open("meta/" + gen + "-url.out", 'a') as u:
            u.write(k+"\n")
n = 1
for i in range(0, len(urls)):
    r = requests.get(str(urls[i]))
    time.sleep(1)
    # time.sleep(.2)
    if r.status_code == 200:
        folder = "test" if i < round(0.2*len(urls)) else "train"
        with open(folder + "/" + gen + "-" + str(n) + ".out", 'a') as fi:
            fi.write(r.content)
            n += 1
            print(n)
    else:
        print('API ERROR')
        print("...on " + urls[i])
