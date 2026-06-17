import re
import actions as ac
import difflib
from HCscript import HCS
import phone_assist as assist
from log_handler import log_and_guard

command_list = [
    "open youtube",
    "play", "search",
    "open gemini",
    "open claude",
    "open chatgpt",
    "open github",
    "open spotify",
    "system info",
    "what time",
    "on my phone"
    ]

class Parser():
    
    def __init__(self):
        pass
        
    #@log_and_guard
    def parse(self, command):
        match_query = re.search(r"play (.+) on youtube", command)
        if match_query:
            query = match_query.group(1)
            return ac.play_youtube(query)
            
        match_query2 = re.search(r"search (.+) on ", command)
        if match_query2:
            query = match_query2.group(1)
            return ac.search_google(query)
        
        match_query3 = re.search(r"open gemini", command)
        if match_query3:
            return ac.open_google_gemini()
    
        match_query4 = re.search(r"open claude", command)
        if match_query4:
            return ac.open_claude()
            
        match_query5 = re.search(r"open chatgpt", command)
        if match_query5:
            return ac.open_chatgpt()
            
        match_query6 = re.search(r"open spotify", command)
        if match_query6:
            return ac.open_spotify()
        
        match_query7 = re.search(r"open github", command)
        if match_query7:
            return ac.github_profile()
            
        match_query8 = re.search(r"open youtube", command)
        if match_query8:
            return ac.open_youtube()
           
        sys_info = re.search(r"system info", command) 
        if sys_info:
            return ac.system_info()
            
        time_info = re.search(r"what time", command)    
        if time_info:
            return ac.time_query()
            
        phone_assistance = re.search(r"(.+) on my phone", command)
        if phone_assistance:
            cmd = phone_assistance.group(1)
            return assist.send_command(cmd)
            
            
        close = difflib.get_close_matches(command, command_list, n=1, cutoff=0.6)
        if close:
                return self.parse(close[0])
                
                
        self.hcs = HCS()
        return self.hcs.handle_replies(command)
        
       
                
        