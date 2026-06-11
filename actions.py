#this is logic file
import webbrowser
import os

def open_youtube():
    url = f"https://www.youtube.com/"
    webbrowser.open(url)
    return f"[SUCCESS] Opened YouTube..."

def play_youtube(query_youtube):
    clean_query = query_youtube.strip().replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={clean_query}"
    webbrowser.open(url)
    return f"[SUCCESS] Opened YouTube For Query : {query_youtube}"


def search_web(query_web):
    clean_query = query_web.strip().replace(" ", "+")
    url = f"https://www.google.com/search?q={clean_query}"
    webbrowser.open(url)
    return f"[SUCCESS] Opened Google For Query : {query_web}"


def open_chatgpt():
    url = f"https://www.chatgpt.com/"
    webbrowser.open(url)
    return f"[SUCCESS] Opened ChatGPT..."

def open_google_gemini():
    url = f"https://gemini.google.com/"
    webbrowser.open(url)
    return f"[SUCCESS] Opened Google Gemini..."

def open_claude():
    url = f"https://www.claude.ai/"
    webbrowser.open(url)
    return f"[SUCCESS] Opened Claude..."

def github_profile(query_github):
    url = f"https://www.github.com/"
    webbrowser.open(url)
    return f"[SUCCESS] Opened GitHub..."

def open_spotify(query_spotify):
    clean_query = query_web.strip().replace(" ", "+")
    url = f"https://www.spotify.com/"
    webbrowser.open(url)
    return f"[SUCCESS] Opened Spotify..."



