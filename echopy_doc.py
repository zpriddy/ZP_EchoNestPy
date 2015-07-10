main_page='''
This is the EchoPy API for Amazon Echo <br> 
All resuests should be made to https://server/EchoPyAPI/
'''
NotNestUser = {"outputSpeech": {"type":"PlainText","text":"Current user is not a valid nest user. Please look for help"},"card":{"type":"Simple","title":"Nest Control Error","content":"Current user is not a valid nest user. Please look for help"},'shouldEndSession':True}