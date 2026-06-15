""" This is a temporary hardcoded scripted area where few replies are handled """ 
import re
import difflib

accepted_query = [
    "hey", "hii", "hello", "hlo",
    "commands",
    "damnn",
    "nope"
]

class HCS():
    def handle_replies(self, user_query):
        
        close_match = difflib.get_close_match(user_query, accepted_query, n=1, cutoff=0.5')
        if close_match:
            return self.handle_replies(close[o])
        
        greet = re.search(r"hey", user_query)
        if greet:
            return f"Hello Sir,\nHow can I assist you today?"
         
        command_query = re.search(r"commands", user_query)   
        if command_query:
            return "commands are..."
         
        shock1 = re.search(r"damnn", user_query) 
        if shock1:
            return f"You seemed to be shocked, are there any scecific reasons"
            
        thanks = re.search(r"thanks bro", user_query)
        if thanks:
            return f"My pleasure to help you :) ."
            
        no = re.search(r"nope", user_query)
        if no:
            return "Okay, let me know if you need any kind of assistance.\nEnjoy... "
         
         
        return f"Command not supported yet"
           