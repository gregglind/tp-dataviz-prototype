#from mrjob.job import MRJob
import json
import string
import ast

class Parser(): 

    
    def stringify(self, event):
        return event[1] + "&" + event[2] + "&" + event[3]
    
    
    def parse(self, display, menubar, eventtype):
        input_file = "desktop_heatmap_users.csv"
        output_file = "user_data_parsed.json"
    
        input_fh = open(input_file, "r")    
        out_fh = open(output_file, "w")        
        user_counts = []
                
        for user in input_fh:            
            #get rid of non-jsony id
            if user == "\n":
                continue
            user = user.split('\t')[1]
            
            #deal with funkiness of trues/falses to let us json load
            ##FIX
            user = string.replace(user, "false", '"False"')
            user = string.replace(user, "true", '"True"')
            user = string.replace(user, '""False""', '"False"')
            user = string.replace(user, '""True""', '"True"')
            user = json.loads(user)["events"]
                        
            counts = {}
            states_observed = []
               
            menu_bar_hidden = None
                     
            for event in user:
                
##commented out menu picks for right now

                if event[0] == 1:
                    event_string = self.stringify(event)
                    output_strings = []
                    
                    if display == "menu":
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
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
##                        
                    
                    else:
                        if event_string in ["site-id-button&&extended validation", "site-id-button&&SSL", "site-id-button&&none"]:
                            elemid = "site-id-button"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                        
    ##                    elif event_string == "back-button&dropdown menu&mouse pick":
    ##                        ##
    ##                        elemid = "back-button-menu"
    ##                        event_string = "heatmap:" + elemid + "#" + event_string
        
                        elif event_string in ["searchbar&go button&click", "searchbar&&no suggestion", "searchbar&&choose suggestion", "searchbar&&enter key","search engine dropdown&menu item&click", "search engine dropdown&menu item&menu pick"]:
                            elemid = "searchbar"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                            
                            if event_string in ["searchbar&&choose suggestion"]:
                                elemid = "searchbar-choose-suggestion"
                                output_strings.append("heatmap:" + elemid + "#" + event_string)
                                
                            if event_string == "search engine dropdown&menu item&click":
                                elemid = "searchbar-search-engine-dropdown"
                                output_strings.append("heatmap:" + elemid + "#" + event_string)    
                            
                            if event_string == "search engine dropdown&menu item&menu pick":
                                elemid = "searchbar-pick-new-search-engine"
                                output_strings.append("heatmap:" + elemid + "#" + event_string)    
    
    
                        elif event_string in ["urlbar&search term&enter key", "urlbar&url&enter key"]:
                            elemid = "urlbar"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                            #this is broken :(
                        
                        elif event_string == "bookmark toolbar&personal bookmark&click":
                            elemid = "bookmark-toolbar"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
    
                        
                        elif event_string in ["urlbar&&choose suggestion", "urlbar&&no suggestion", "urlbar&search term&go button click", "urlbar&url&go button click", "urlbar-go-button&&click"]:
                            elemid = "urlbar"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                               
                                
                            if event_string in ["urlbar&search term&go button click", "urlbar&url&go button click", "urlbar-go-button&&click"]:
                                elemid = "urlbar-go-button"
                                output_strings.append("heatmap:" + elemid + "#" + event_string)
                            
                            if event_string in ["urlbar&&choose suggestion"]:
                                elemid = "urlbar-choose-suggestion"
                                output_strings.append("heatmap:" + elemid + "#" + event_string)    
                        
    
                        
                        elif event_string == "urlbar&most frequently used menu&open":
                            ##
                            elemid = "most-frequent-menu"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                        
                        elif event_string == "tabbar&new tab button&click":
                            elemid = "new-tab-button"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                            
                        elif event_string == "tabbar&drop down menu&click":
                            elemid = "alltabs-button"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                        
                        elif event_string == "Panorama&Tab View Interface&Opened":
                            states_observed.append(event_string)
                            
                        elif event_string == "Panorama&Tab View Interface&Closed":
                            if "Panorama&Tab View Interface&Opened" in states_observed:
                                states_observed.remove("Panorama&Tab View Interface&Opened")
                                elemid = "menu-tabview"
                                output_strings.append("heatmap:" + elemid + "#" + "Panorama&Tab View Interface&Toggled")
                        
                        elif event_string == "bookmarks-menu-button&bookmarks-menu-button&click" and menubar == "hidden":
                            states_observed.append(event_string)
                            continue
                        
                        elif event_string == "bookmarks-menu-button&&click"  and menubar == "hidden":
                            if "bookmarks-menu-button&bookmarks-menu-button&click" in states_observed:                            
                                states_observed.remove("bookmarks-menu-button&bookmarks-menu-button&click")
                                states_observed.append(event_string)
                                continue
                        
                        elif event_string == "bookmarks-menu-button&personal bookmark&click" and menubar == "hidden":
                            if "bookmarks-menu-button&&click" in states_observed:
                                states_observed.remove("bookmarks-menu-button&&click") 
                                elemid = "bookmarks-menu-button"
                                output_strings.append("heatmap:" + elemid + "#" + event_string)
                            else:
                                elemid = "bookmarks-menu-button"
                                output_strings.append("heatmap:" + elemid + "#" + event_string)
    
                        
    ##                    elif event_string == "tabbar&left scroll button&mousedown":
    ##                        states_observed.append(event_string)
    ##                        continue
    ##                        
    ##                    elif event_string == "tabbar&left scroll button&mouseup":
    ##                        if "tabbar&left scroll button&mousedown" in states_observed:
    ##                            states_observed.remove("tabbar&left scroll button&mousedown")
    ##                            event_string = "tabbar&left scroll button&click"
    ##                        else:
    ##                            continue
    ##                        
    ##                    elif event_string == "tabbar&right scroll button&mousedown":
    ##                        states_observed.append(event_string)
    ##                        continue
    ##                        
    ##                    elif event_string == "tabbar&right scroll button&mouseup":
    ##                        if "tabbar&right scroll button&mousedown" in states_observed:
    ##                            states_observed.remove("tabbar&right scroll button&mousedown")
    ##                            event_string = "tabbar&right scroll button&click"
    ##                        else:
    ##                            continue
                            
                        elif event_string == "star-button&&click":
                            states_observed.append(event_string)
                            
                        elif event_string == "star-button&edit bookmark panel&panel open":
                            states_observed.append(event_string)
                            
                        elif event_string == "star-button&remove bookmark button&click":
                            if "star-button&&click" in states_observed and "star-button&edit bookmark panel&panel open" in states_observed:
                                states_observed.remove("star-button&&click") 
                                states_observed.remove("star-button&edit bookmark panel&panel open")
                                elemid = "star-button"
                                output_strings.append("heatmap:" + elemid + "#" + event_string)
                                                      
                                                      
    
    ##                    elif event[1] == "menus" and event[3] == "key shortcut":
    ##                        elemid = string.replace(event[2], "key", "menu")
    ##                        event_string = "heatmap:" + elemid + "#" + event_string
    ##                        
    ##                    elif event[1] == "tab context menu" and event[3] == "click":
    ##                        elemid = event[2]
    ##                        event_string = "heatmap:" + elemid + "#" + event_string
    ##                        
    ##                    elif event[1] == "contentAreaContextMenu" and event[3] == "click":
    ##                        elemid = event[2]
    ##                        event_string = "heatmap:" + elemid + "#" + event_string
    ##                        
    ##                    elif event[1] == "contentAreaContextMenu" and event[3] == "mouse":
    ##                        elemid = event[2]
    ##                        event_string = "heatmap:" + elemid + "#" + event_string
    ##                        
                        elif event[2] == "" and event[3] == "click":
                            if event[1] == "bookmarks-menu-button" and menubar == "shown":
                                continue
                            elemid = event[1]
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                            
                        elif event[1] == "feedback-toolbar" and event[3] == "click":
                            elemid = "feedback-toolbar"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
        
                        elif event[1] == "urlbar" and event[2][0:11] == "moz-action:" and event[3] == "enter key":
                            elemid = "urlbar"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                        
                        elif event[1] == "urlbar" and event[2][0:11] == "moz-action:" and event[3] == "go button click":
                            elemid = "urlbar"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                            elemid = "urlbar-go-button"
                            output_strings.append("heatmap:" + elemid + "#" + event_string)
                        
    ##                    elif event[2] == "slider" and event[3] == "drag":
    ##                        elemid = "-".join(event[1].split())
    ##                        output_strings.append("heatmap:" + elemid + "#" + event_string)
    ##
    ##                    elif event[2] == "up scroll button" and event[3] == "click":
    ##                        elemid = "-".join(event[1].split())
    ##                        output_strings.append("heatmap:" + elemid + "#" + event_string)
    ##                        
    ##                    elif event[2] == "down scroll button" and event[3] == "click":
    ##                        elemid = "-".join(event[1].split())
    ##                        output_strings.append("heatmap:" + elemid + "#" + event_string)
                       
                        else:
                            #do nothing
                            pass
                    
                    for s in output_strings:
                        if s in counts:
                            counts[s] += 1
                        else:
                            counts[s] = 1
                    
                if event[0] == 3:
                    if event[1] == "menu bar" and event[2] == "hidden?":
                        if event[3] == "False":
                            menu_bar_hidden = False
                        else:
                            menu_bar_hidden = True
                        
                        
                    config = "config:" + event[1] + "&" + event[2]
                    changed_config = "config_changed:" + event[1] + "&" + event[2]
                    if config in counts and counts[config] != event[3]:
                        del counts[config]
                        counts[changed_config] = event[3]
                    elif changed_config in counts and counts[changed_config] != event[3]:             
                        counts[changed_config] = event[3]
                    else:
                        counts[config] = event[3]
             
            #wrap up any uncompleted states   
            
            if "bookmarks-menu-button&&click" in states_observed:
                if "bookmarks-menu-button&&click" in counts:
                    counts["heatmap:bookmarks-menu-button#bookmarks-menu-button&&click"] += 1
                else:
                    counts["heatmap:bookmarks-menu-button#bookmarks-menu-button&&click"] = 1
            
            
            if "star-button&&click" in states_observed:
                
                if "star-button&&click" in counts:
                    counts["heatmap:star-button#star-button&&click"] += 1
                else:
                    counts["heatmap:star-button#star-button&&click"] = 1
            
            #does the menu bar attribute comply? if not, skip over
            if menu_bar_hidden is None:
                #should only happen when the user is empty
                continue
            
            elif menu_bar_hidden is False:
                if menubar == "hidden":
                    continue
                
            elif menu_bar_hidden is True:
                if menubar == "shown":
                    continue
                
            
            user_counts.append(counts)

        out_fh.write(json.dumps(user_counts))
        out_fh.close()
    
if __name__ == '__main__':
    import sys
    if sys.argv[1] in ("window", "menu") and sys.argv[2] in ("hidden", "shown") and sys.argv[3] in ("clicks", "shortcut"):
        p = Parser()
        p.parse(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "arguments are incorrect"