import webbrowser
import os
import psutil
import datetime

def time_query():
    time = datetime.datetime.now().strftime("%I:%M:%S:%p")
    return f"Current Time is: {time}"

def  system_info():
    battery = psutil.sensors_battery()
    ram = psutil.vertual_memory()
    cpu = psutil.cpu_percent(interval=1)
    
    return f""" [——SYSTEM    INFO——]
    Battery: {battery.percent}% {'(Charging)' if battery.power_plugged else '(Discharging)'}
    RAM: {ram.percent}% used
    CPU: {cpu}%
    """

def open_youtube(query):
    url = f"https://www.youtube.com/"
    webbrowser.open(url)
    terminal = f"[SUCCESS] Opened YouTube"
    chat = f"Sure Sir,\nI\'ve opened YouTube for you."
    return terminal, chat

def play_youtube(query_youtube):
    if query_youtube == None:
        return open_youtube()
    else:
        #clean_query = query_youtube.strip().replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query_youtube}"
        webbrowser.open(url)
        terminal = f"[SUCCESS] Opened Yourube For Query : {query_youtube}"
        chat = f"Sure Sir,\nI\'ve opened YouTUbe and searched {query_youtube} for you. "
        return terminal, chat


def search_google(query_web):
    if query_web == None:
        webbrowser.open("https://www.google.com/")
        terminal = f"[SUCCESS] Opened Google.[no query was given]"
        chat = f"Sure Sir,\nI\'ve opened Google for you. "
        return terminal, chat
        
    else:
        #clean_query = query_web.strip().replace(" ", "+")
        url = f"https://www.google.com/search?q={query_web}"
        webbrowser.open(url)
        terminal = f"[SUCCESS] Opened Google For Query : {query_web}"
        chat = f"Sure Sir,\nI\'ve opened Google and searched {query_web} for you. "
        return terminal, chat


def open_chatgpt(query):
    url = f"https://www.chatgpt.com/"
    webbrowser.open(url)
    terminal = f"[SUCCESS] Opened ChatGPT"
    chat = f"Sure Sir,\nI\'ve opened ChatGPT for you. "
    return terminal, chat

def open_google_gemini(query):
    url = f"https://gemini.google.com/"
    webbrowser.open(url)
    terminal = f"[SUCCESS] Opened Google Gemini"
    chat = f"Sure Sir,\nI\'ve opened Google Gemini for you. "
    return terminal, chat

def open_claude(query):
    url = f"https://www.claude.ai/"
    webbrowser.open(url)
    terminal = f"[SUCCESS] Opened Claude"
    chat = f"Sure Sir,\nI\'ve opened Claude for you. "
    return terminal, chat

def open_github(query):
    url = f"https://www.github.com/dev-shivv/Assistant-Framework.git"
    webbrowser.open(url)
    terminal = f"[SUCCESS] Opened dev-shivv\'s GitHub"
    chat = f"Sure Sir,\nI\'ve opened your GitHub Repo of this project for you. "
    return terminal, chat

def open_spotify(query_spotify):
    clean_query = query_web.strip().replace(" ", "+")
    url = f"https://www.spotify.com/"
    webbrowser.open(url)
    terminal = f"[SUCCESS] Opened Spotify"
    chat = f"Sure Sir,\nI\'ve opened Spotify for you. "
    return terminal, chat



