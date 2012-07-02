from itertools import chain
import simplejson
import fileinput
from collections import Counter, defaultdict

# globals, yay!
me = []
C = Counter()
Longrunners = Counter()

prev = 0
hasany = set()

def complete():
    global me
    lastaction = ('(unknown)','','')
    if 'back' not in me[-1]:
        lastaction = tuple(me.pop(-1)[1][:3])

    n = len(me)
    C[n] += 1
    if n >= 4:
        Longrunners[lastaction] += 1

    if n > 100: print "LONG\n", "\n".join(map(str,me))
    me = []

for line in fileinput.input():
    line = line.strip()
    if line == "--":
        complete()
    else:
        d = simplejson.loads(line)
        me.append(d)
        hasany.add(d[0])


def summary(counts):
    n = sum(counts.values())
    mean = sum((k*v for k,v in counts.iteritems()))   / float(n)
    # ugh! turn back into list...
    indices = [int(k * n) for k in (.05,.25,.50,.75,.95)]
    reexpanded = list(chain(*([k,]*v for (k,v) in sorted(counts.iteritems()))))
    qs = [reexpanded[i] for i in indices]

    return n,mean,qs


n = sum(C.values())
print C.most_common()
for k in sorted(C.iteritems()):
    k1 = list(k[:]) + [k[1]/float(n),]
    print '{0}\t{2:.1%}\t{1}'.format(*k1)

nr = sum(Longrunners.values())
for k in Longrunners.most_common(20):
    k1 = list(k[:]) + [k[1]/float(nr),]
    print '{0}\t{2:.1%}\t{1}'.format(*k1)



print "hasany", len(hasany)
print summary(C)



TODO = """

for 'long' (4 or more), what do they do at the end of it?
break up 'long runs', and ensure we aren't 'mingling'
get 'event' code from Ilana.

does swipe trigger the back button in this study?

back button is very popular (of 85% usage)

sequences of clicks can imply user desire, without asking them.
"""


print TODO
