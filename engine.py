import re
import actions as logic



while True:
    command = input("Input Command :").lower().strip()
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
        logic.play_youtube(query)

    elif match_query2:
        query = match_query2.group(1)
        logic.search_web(query)
    
    elif match_query3:
        # query = match_query3.group(1)
        logic.open_google_gemini()

    elif match_query4:
        # query = match_query4.group(1)
        logic.open_claude()

    elif match_query5:
        # query = match_query5.group(1)
        logic.open_chatgpt()

    elif match_query6:
        # query = match_query6.group(1)
        logic.open_spotify()

    elif match_query7:
        # query = match_query7.group(1)
        logic.open_github()

    elif match_query8:
        # query = match_query8.group(1)
        logic.open_youtube()


    else:
        print("Invalid Command")