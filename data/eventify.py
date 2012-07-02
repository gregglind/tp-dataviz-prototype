import simplejson
import csv
from itertools import chain
import fileinput
#import random
import hashlib
import time

def tryparse(json):
    try:
        return simplejson.loads(json)
    except:
        return None

def parse_input_file(fh):
    """

    """
    return filter(None,(tryparse(l.strip().split('\t')[1]) for l in fh))

LASTEVENT='THISISTHELASTEVENT'


def map_events_for_person(in_events):
    """ yields a gen of summarized events.

    This duplicates (badly) ilana's code, sadly
    """
    # [1, 'window', '4', 'window closed', 1335290155985]
    # [1, 'menus', 'key_newNavigatorTab', 'key shortcut', 1335292079565],

    def stringify(event):  return "&".join(map(str,event))

    in_events = list(in_events) # no generators here.
    for (ii,x) in enumerate(in_events):
        #print x
        t,area,sub1,sub2,ts = x
        event = x

        # special cases
        if t == 3:  continue # stats, counts, etc.
        if t == 0:  continue # study startup, etc.

        ## gory gory details...
        ## TODO clean up.
        elemid = '--'
        if event[1] in ["menu_FilePopup", "historyUndoMenu", "historyUndoWindowMenu", "file-menu", "menu_EditPopup", "menu_viewPopup", "view-menu", "goPopup", "tools-menu", "history-menu", "menu_ToolsPopup", "bookmarksMenu", "bookmarksMenuPopup", "windowPopup", "menu_HelpPopup", "helpMenu", "windowMenu"] and event[3] == "mouse":
            if event[1] == "windowMenu" and event[2][:6] == "window":
                elemid = "go-to-window"
            elif event[1] == "bookmarksMenu" and event[2] == "user-defined item":
                elemid = "personal-bookmarks"
            elif event[1] == "history-menu" and event[2] == "user-defined item":
                elemid = "recently-visited-pages"
            elif event[1] == "historyUndoMenu" and event[2] == "user-defined item":
                elemid = "recently-closed-tabs"
            elif event[1] == "historyUndoWindowMenu" and event[2] == "user-defined item":
                elemid = "recently-closed-windows"
            else:
                elemid = event[2]

        yield area,sub1,sub2,elemid, ts

    yield LASTEVENT,'','',0  # a sigil

from collections import Counter, defaultdict

def pairs(C,gen):
    """ on a person!  assumes only one LASTEVENT per """
    first = gen.next()
    for second in gen:
        if second == LASTEVENT:
            break
        else:
            C[first][second] +=1
            first = second

    return None # side effect, gross

## we gots to do this matrix style, alas.
def outfiles(C,fn_csv,fn_adj_json, fn_adj_json2):
    """ outputs csv and json of corrmatrix"""

    ## all have to appear on both sides... full adj matrix
    K = list(chain(*[C[x].keys() for x in C.keys()])) + C.keys()
    K = sorted(set(K))

    with open(fn_csv,'w') as fh_csv:
        fh_csv = csv.writer(fh_csv)
        fh_csv.writerow(['name','color'])
        for k in K:
            #fh_csv.writerow(k,"%s" % (hex(random.getrandbits(8*3)[2:])))
            color = "#"+ hashlib.md5(k).hexdigest()[:6]
            fh_csv.writerow([k,color])

    s = float(sum([sum(C[k].values())for k in K]))
    matrix = []
    for k in K:
        my = C[k]
        pcts = [my[j] / s for j in K]
        matrix.append(pcts)

    simplejson.dump(matrix, open(fn_adj_json,'w'),indent=2)

    matrix2 = []  # within group pcts
    for k in K:
        my = C[k]
        s = float(sum(my.values()))
        pcts = [my[j] / s for j in K]
        matrix2.append(pcts)

    simplejson.dump(matrix2, open(fn_adj_json2,'w'),indent=2)

    return True


def main(fn):
    people = parse_input_file(fn)
    events = (x['events'] for x in people)
    meta_gen = (map_events_for_person(x) for x in events)
    #C = defaultdict(Counter)
    #modify C by side-effect
    #for gen in meta_gen:  pairs(C,gen)
    #outfiles(C,'actions.csv','matrix.json','matrix2.json')
    for (ii,gen) in enumerate(meta_gen):
        for x in gen:
            print simplejson.dumps([ii,x,time.ctime(float(x[-1]/1000)).strip()])

if __name__ == "__main__":
    main(fileinput.input())
