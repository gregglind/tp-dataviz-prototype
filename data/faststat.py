"""
args:
   needle [...] filename
"""

import fileinput
import simplejson
from collections import Counter
from itertools import chain
from math import floor

# for each line, does it match
# record % of people having it
# record distribution of use for people having it


def summary(counts):
    n = sum(counts.values())
    p = len(counts)
    mean = n / float(p)
    indices = [int(floor(k * p)) for k in (.05,.25,.50,.75,.95)]
    reexpanded = sorted(counts.itervalues())
    qs = [reexpanded[i] for i in indices]

    return n,mean,qs


# this is sloppy parse bs
# we could be smarter here and do all events at once.
def faststat(needle,lines):
    n = 0
    allids = set()
    C = Counter()
    for line in lines:
        n += 1
        person,evt,timestr = simplejson.loads(line.strip())
        allids.add(person)
        if needle in line:
            C[person] += 1

    return dict(needle=needle, nevents=n,npeople=len(allids),pct=100*float(len(C))/len(allids), summary=summary(C))

if __name__ == "__main__":
    import sys
    needles = sys.argv[1:-1]
    for n in needles:
        print faststat(n,open(sys.argv[-1]))

