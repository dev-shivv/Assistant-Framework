from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import difflib
import os

PORT = 8080
CUTOFF = 0.4

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip() or result.stderr.strip() or "Done"

COMMANDS = {
    "turn on flash"         : lambda: run("termux-torch on"),
    "turn off flash"        : lambda: run("termux-torch off"),
    "flashlight on"         : lambda: run("termux-torch on"),
    "flashlight off"        : lambda: run("termux-torch off"),
    "torch on"              : lambda: run("termux-torch on"),
    "torch off"             : lambda: run("termux-torch off"),
    "volume up"             : lambda: run("termux-volume music 15"),
    "volume down"           : lambda: run("termux-volume music 5"),
    "mute"                  : lambda: run("termux-volume music 0"),
    "max volume"            : lambda: run("termux-volume music 15"),
    "open youtube"          : lambda: run("am start -a android.intent.action.VIEW -d 'https://youtube.com'"),
    "open instagram"        : lambda: run("am start -n com.instagram.android/.activity.MainTabActivity"),
    "open whatsapp"         : lambda: run("am start -n com.whatsapp/.HomeActivity"),
    "open telegram"         : lambda: run("am start -n org.telegram.messenger/.DefaultIcon"),
    "open settings"         : lambda: run("am start -a android.settings.SETTINGS"),
    "open camera"           : lambda: run("am start -a android.media.action.IMAGE_CAPTURE"),
    "open gallery"          : lambda: run("am start -a android.intent.action.VIEW -t image/*"),
    "open maps"             : lambda: run("am start -a android.intent.action.VIEW -d 'geo:0,0'"),
    "open chrome"           : lambda: run("am start -n com.android.chrome/com.google.android.apps.chrome.Main"),
    "open spotify"          : lambda: run("am start -n com.spotify.music/.MainActivity"),
    "open google assistant" : lambda: run("am start -a android.intent.action.VOICE_COMMAND"),
    "open calculator"       : lambda: run("am start -a android.intent.action.MAIN -c android.intent.category.APP_CALCULATOR"),
    "open clock"            : lambda: run("am start -a android.intent.action.MAIN -c android.intent.category.APP_ALARM_CLOCK"),
    "open contacts"         : lambda: run("am start -a android.intent.action.MAIN -c android.intent.category.APP_CONTACTS"),
    "open files"            : lambda: run("am start -a android.intent.action.MAIN -c android.intent.category.APP_FILES"),
    "open termux"           : lambda: run("am start -n com.termux/.HomeActivity"),
    "open google"           : lambda: run("am start -a android.intent.action.VIEW -d 'https://google.com'"),
    "open github"           : lambda: run("am start -a android.intent.action.VIEW -d 'https://github.com'"),
    "open reddit"           : lambda: run("am start -a android.intent.action.VIEW -d 'https://reddit.com'"),
    "open twitter"          : lambda: run("am start -a android.intent.action.VIEW -d 'https://twitter.com'"),
    "wifi on"               : lambda: run("svc wifi enable"),
    "wifi off"              : lambda: run("svc wifi disable"),
    "enable wifi"           : lambda: run("svc wifi enable"),
    "disable wifi"          : lambda: run("svc wifi disable"),
    "bluetooth on"          : lambda: run("svc bluetooth enable"),
    "bluetooth off"         : lambda: run("svc bluetooth disable"),
    "battery status"        : lambda: run("termux-battery-status"),
    "what is battery"       : lambda: run("termux-battery-status"),
    "battery level"         : lambda: run("termux-battery-status"),
    "check battery"         : lambda: run("termux-battery-status"),
    "storage info"          : lambda: run("df -h /sdcard"),
    "check storage"         : lambda: run("df -h /sdcard"),
    "memory info"           : lambda: run("free -h"),
    "check ram"             : lambda: run("free -h"),
    "ip address"            : lambda: run("ip addr show wlan0 | grep 'inet '"),
    "what is my ip"         : lambda: run("ip addr show wlan0 | grep 'inet '"),
    "send notification"     : lambda: run("termux-notification --title 'Sh1v' --content 'Hey from your assistant'"),
    "test notification"     : lambda: run("termux-notification --title 'Sh1v' --content 'Connection is working!'"),
    "take screenshot"       : lambda: run("termux-screenshot"),
    "vibrate"               : lambda: run("termux-vibrate -d 500"),
    "say hello"             : lambda: "Hello from Sh1v phone server!",
    "ping"                  : lambda: "pong",
    "status"                : lambda: "Sh1v server is running fine.",
}

def parse_command(text: str):
    text = text.lower().strip()
    keys = list(COMMANDS.keys())
    matches = difflib.get_close_matches(text, keys, n=1, cutoff=CUTOFF)
    if matches:
        return matches[0], difflib.SequenceMatcher(None, text, matches[0]).ratio()
    for key in keys:
        if key in text or text in key:
            return key, 0.5
    return None, 0

def execute_command(key: str):
    try:
        result = COMMANDS[key]()
        return str(result
