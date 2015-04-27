#!/usr/bin/python
import requests
import time
import math
import sys


with open(sys.argv[1], "r") as f:
    urls = []
    for line in f:
        k ="https://okcupid.com/profile/"+line.strip('\n')
        urls.append(k)
        with open(sys.argv[2], 'a') as u:
            u.write(k+"\n")
