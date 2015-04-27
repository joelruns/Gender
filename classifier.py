from __future__ import division
from os import walk
from stemming.porter2 import stem
import os, sys, re, numpy as np

# Get data filenames
fns, ws, wa, fwa, mwa, pm = [[], [], [], [], [], 0.0]
try:
    os.remove("train/.DS_Store")
    os.remove("test/.DS_Store")
except OSError:
    pass
for (dirpath, dirnames, filenames) in walk("train"):
    fns.extend(filenames)
    break
for (dirpath, dirnames, filenames) in walk("test"):
    fns.extend(filenames)
    break

# Format data
for f in fns:
    try:
        p, cat = [open("train/" + f).read(), "train"]
    except IOError:
        p, cat = [open("test/" + f).read(), "test"]
    user = re.search('id="basic_info_sn" class="name ">(.+?)</span>', p).group(1)
    gender = re.search('<span class="ajax_gender">(.+?)</span>', p).group(1)
    if "Wo" not in gender:
        pm = pm + 1
    text = ""
    for i in range(0, 10):
        s = 'essay_text_'+ str(i) +'" class="essay">(.*?)</div>'
        e = re.search(s, p, re.DOTALL)
        if e != None:
            h = re.sub('<br />', '', e.group(1)).strip()
            h = re.sub('</*?a(.|\n)*?>|</*?b>|</*?i>|</*?u>', '', h)
            h = re.sub('[^\'\w]+', ' ', re.sub(':[\w][\W]', '&', h)).strip()
            text = text + re.sub('[\W]+\'|\'[\W]+', ' ', h) + " "
    text = text.strip().lower()
    text = re.sub('  *', ' ', text)

    # Update word and alpha lists
    texts = text.split()
    for w in texts:
        c = stem(w)
        if c not in ws:
            ws.append(c)
            wa.append(0)
            fwa.append(1)
            mwa.append(1)
        wi = ws.index(c)
        wa[wi] = wa[wi] + 1
        if cat == "train":
            if "Wo" not in gender:
                mwa[wi] = mwa[wi] + 1
            else:
                fwa[wi] = fwa[wi] + 1

    # Sanity check for progress
    sys.stdout.write("\r\x1b[2K" + "Words: " + str(len(ws)) + " - " + user)
    sys.stdout.flush()

# Posterior probability
pm = pm / len(fns)
wt = sum(wa)
fds = np.random.dirichlet(fwa, 20)
mds = np.random.dirichlet(mwa, 20)
def getPos(words, gds, gen):
    gdt = len(gds)
    pgd, pws = [0, 0]
    for word in words:
        wi = ws.index(stem(word))
        pws = pws + np.log(wa[wi] / wt)
        total = 0
        for gd in gds:
            total = total + gd[wi]
        pgd = pgd + np.log(total / gdt)
    if gen == 'm':
        return np.exp(pgd + np.log(pm) - pws)
    else:
        return np.exp(pgd + np.log(1-pm) - pws)

# Prediction sanity checks
s = "nurse sensitive flowers"
print "\n\nSanity: " + s
print "Girl: " + str(getPos(s.split(), fds, 'f'))
print "Boy: " + str(getPos(s.split(), mds, 'm')) + '\n'
s = "gamer dirt bike"
print "Sanity: " + s
print "Girl: " + str(getPos(s.split(), fds, 'f'))
print "Boy: " + str(getPos(s.split(), mds, 'm'))
print "\nDing your toast is ready!"

# Testing set
tns, fa, ta, tt = [[], 0, 0, 0]
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

    # Make a guess
    firsts, texts = [first.split(), text.split()]
    try:
        fposf, fposm = [getPos(firsts, fds, 'f'), getPos(firsts, mds, 'm')]
        tposf, tposm = [getPos(texts, fds, 'f'), getPos(texts, mds, 'm')]
        if fposf > fposm:
            fg = "Woman"
        if tposf > tposm:
            tg = "Woman"
        if ("Wo" in gender) ^ (fg == "Man"):
            fa = fa + 1
        else:
            trunc = (first[:60] + '...') if len(first) > 60 else first
            print "- Wrong: " + trunc
            print "  " + gender
            print "  Girl: " + str(fposf)
            print "  Boy: " + str(fposm)
        if ("Wo" in gender) ^ (tg == "Man"):
            ta = ta + 1
        tt = tt + 1
    except ValueError, e:
        pass

# Print results
fa, ta = [round(fa / tt * 100, 1), round(ta / tt * 100, 1)]
print "\nTest results over " + str(tt) + " sentences"
print "First sentence: " + str(fa) + "%"
print "Whole profiles: " + str(ta) + "%\n"

# Play around with system
while True:
    inputs = raw_input("Master your command: ").lower().split()
    if inputs[0] == "#quit":
        sys.exit(0)
    try:
        posf, posm = [getPos(inputs, fds, 'f'), getPos(inputs, mds, 'm')]
        if posf > posm:
            print "- Girl by " + str(round(posf / posm * 100, 1)) + "%"
        else:
            print "- Boy by " + str(round(posm / posf * 100, 1)) + "%"
    except ValueError, e:
        print "- " + str(e)
