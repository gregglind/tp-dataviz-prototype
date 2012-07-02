# Example Usage

    head -n20 desktop_heatmap_2012.json | python eventify.py > events.txt
    python faststat.py ` grep send context-menu.txt | cut -d, -f3 | sort | uniq | xargs` events.txt


# Main ideas / design goals:

* filter for 'stream of events'
* multiple input lines might be 'one event' here.
* transform for 'simple stats'
* more generators
* separate the 'generate stream of events' from the 'map this to
heatmap'
* events should be 'logical' / semantic
* one event per line, so there is a hope in heaven of using grep on them
* 'terminal events'?  Is this a good idea or not?
    - it means that users with no events show up
    - easy to grep for
    - but a little gross (see:  null strings in C)
* 'more attributes' should be 'extra' (like type of click?  num
windows?).  Specficially, events should be able to be rolled up several
ways?
* events in the output should be 'independent'?
* should we call out 'inferred events' (like shutdown, switch window?)

