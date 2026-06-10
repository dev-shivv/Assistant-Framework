import re
import actions as ac

def parse(command):
    
    match_query = re.search(r"play (.+) on youtube", command)
    match_query2 = re.search(r"search (.+) on google", command)
    match_query3 = re.search(r"open gemini", command)
    match_query4 = re.search(r"open claude", command)
    match_query5 = re.search(r"open chatgpt", command)
    match_query6 = re.search(r"open spotify", command)
    match_query7 = re.search(r"open github", command)
    match_query8 = re.search(r"open youtube", command)
    if match_query:
        query = match_query.group(1)
        ac.play_youtube(query)
        return "Opening yt"
 
 
    elif match_query2:
        query = match_query2.group(1)
        ac.search_web(query)
        return "Opening YouTube...."
    
    elif match_query3:
        # query = match_query3.group(1)
        ac.open_google_gemini()
        return "Opening YouTube...."

    elif match_query4:
        # query = match_query4.group(1)
        ac.open_claude()
        return "Opening YouTube...."

    elif match_query5:
        # query = match_query5.group(1)
        ac.open_chatgpt()
        return "Opening YouTube...."

    elif match_query6:
        # query = match_query6.group(1)
        ac.open_spotify()
        return "Opening YouTube...."

    elif match_query7:
        # query = match_query7.group(1)
        ac.open_github()
        return "Opening YouTube...."

    elif match_query8:
        # query = match_query8.group(1)
        ac.open_youtube()
        return "Opening YouTube...."



    else:
        print("Invalid Command")
        return "Opening YouTube...."
            