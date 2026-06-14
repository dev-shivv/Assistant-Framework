import re
import actions as ac
import difflib
from HCscript import HCS
#from target_device import PhoneCommand
import phone_assist as remote

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
        
    
    def parse(self, command):
        
        phone_assistance = re.search(r"(.+) on my phone", command)
        if phone_assistance:
            self.cmd = phone_assistance.group(1)
            return remote.send_command(self.cmd)

            
        match_query = re.search(r"play (.+) on youtube", command)
        if match_query:
            query = match_query.group(1)
            return ac.play_youtube(query)
            #return "Playing"
        
        
        match_query2 = re.search(r"search (.+) on ", command)
        if match_query2:
            query = match_query2.group(1)
            return ac.search_web(query)
            #return "Opening Browser..."
        
        match_query3 = re.search(r"open gemini", command)
        if match_query3:
            # query = match_query3.group(1)
            return ac.open_google_gemini()
            #return "Opening Gemini..."
    
        match_query4 = re.search(r"open claude", command)
        if match_query4:
            # query = match_query4.group(1)
            return ac.open_claude()
            #return "Opening Claude...."
            
        match_query5 = re.search(r"open chatgpt", command)
        if match_query5:
            # query = match_query5.group(1)
            return ac.open_chatgpt()
            #return "Opening ChatGPT...."
            
        match_query6 = re.search(r"open spotify", command)
        if match_query6:
            # query = match_query6.group(1)
            return ac.open_spotify()
            #return "Opening Spotify...."
        
        match_query7 = re.search(r"open github", command)
        if match_query7:
            # query = match_query7.group(1)
            return ac.github_profile()
            #return "Opening GitHub...."
            
        match_query8 = re.search(r"open youtube", command)
        if match_query8:
            # query = match_query8.group(1)
            return ac.open_youtube()
            #return "Opening YouTube...."
           
        sys_info = re.search(r"system info", command) 
        if sys_info:
            return ac.system_info()
            
        time_info = re.search(r"what time", command)    
        if time_info:
            return ac.time_query()
            
        close = difflib.get_close_matches(command, command_list, n=1, cutoff=0.6)
        if close:
                return self.parse(close[0])
                
                
        self.hcs = HCS()
        return self.hcs.handle_replies(command)
        
       
                
        