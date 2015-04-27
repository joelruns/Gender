from __future__ import division
from os import walk
from stemming.porter2 import stem
import os, sys, re, numpy as np

# Get sentences from test
tns, fc, mc = [[], 0, 0]
try:
    os.remove("train/.DS_Store")
    os.remove("test/.DS_Store")
except OSError:
    pass
for (dirpath, dirnames, filenames) in walk("test"):
    tns.extend(filenames)
    break

# Check accuracy
for t in tns:
    text, first, fg, tg = ["", "", "Man", "Man"]
    p = open("test/" + t).read()
    gender = re.search('<span class="ajax_gender">(.+?)</span>', p).group(1)
    for j in range(0, 10):
        s = 'essay_text_'+ str(j) +'" class="essay">(.*?)</div>'
        e = re.search(s, p, re.DOTALL)
        if e != None:
            h = re.sub('<br />', '', e.group(1)).strip()
            h = re.sub('</*?a(.|\n)*?>|</*?b>|</*?i>|</*?u>', '', h)
            h = re.sub('[^\'\w.]+', ' ', re.sub(':[\w][\W]', '&', h)).strip()
            text = text + re.sub('[\W]+\'|\'[\W]+', ' ', h) + " "
    text = text.strip().lower()

    # Get first sentence
    try:
        first = re.search('(.+?)\.', text).group(1)
    except AttributeError:
        first = text
    text = re.sub('  *', ' ', re.sub('\.+?', ' ', text))

    # Get first ten of both genders
    if fc < 10 and "Wo" in gender:
        print gender + ": " + first
        fc = fc + 1
    elif mc < 10 and "Wo" not in gender:
        print gender + ": " + first
        mc = mc + 1

