import re
import actions as ac

class Parser():
    
    def __init__(self):
        pass
    
    def parse(self, command):
        
        
        match_query = re.search(r"play (.+) on youtube", command)
        if match_query:
            query = match_query.group(1)
            ac.play_youtube(query)
            return "Playing"
        
        
        match_query2 = re.search(r"search (.+) on google", command)
        if match_query2:
            query = match_query2.group(1)
            ac.search_web(query)
            return "Opening Browser..."
        
        match_query3 = re.search(r"open gemini", command)
        if match_query3:
            # query = match_query3.group(1)
            ac.open_google_gemini()
            return "Opening Gemini..."
    
        match_query4 = re.search(r"open claude", command)
        if match_query4:
            # query = match_query4.group(1)
            ac.open_claude()
            return "Opening Claude...."
            
        match_query5 = re.search(r"open chatgpt", command)
        if match_query5:
            # query = match_query5.group(1)
            ac.open_chatgpt()
            return "Opening ChatGPT...."
            
        match_query6 = re.search(r"open spotify", command)
        if match_query6:
            # query = match_query6.group(1)
            ac.open_spotify()
            return "Opening Spotify...."
        
        match_query7 = re.search(r"open github", command)
        if match_query7:
            # query = match_query7.group(1)
            ac.open_github()
            return "Opening GitHub...."
            
        match_query8 = re.search(r"open youtube", command)
        if match_query8:
            # query = match_query8.group(1)
            ac.open_youtube()
            return "Opening YouTube...."
        
    

        return "Invalid Command...."
                