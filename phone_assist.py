import requests
#from PySide6.QtCore import QThread, Signal, Slot

def send_command(cmds):
    cmd = f"{cmds}"
    try:
        r = requests.post("http://10.87.170.174:5005/command", 
                          json={"command": cmd})
                          
        req = r.json()
        chat = f"Okay Sir,\nYour query for \"{cmd}\" on your phone is completed."
                          
        return req, chat
        
    except Exception as e:
        return f"ERROR: {str(e)}"
    #thread.start()
    
#send_command()