import json
import nestpy_app
import echopy_doc
import nestpy_lib as nest
import nestpy_settings as settings


appVersion = 1.0


def data_init():
	global MyDataStore
	MyDataStore = DataStore()



def data_handler(rawdata):
	global MyDataStore
	#print rawdata['session']
	currentSession = MyDataStore.getSession(rawdata['session'])
	currentUser = MyDataStore.getUser(rawdata['session'])
	currentRequest = rawdata['request']
	response = request_handler(currentSession, currentUser, currentRequest)


	#print json.dumps({"version":appVersion,"response":response},sort_keys=True,indent=4)

	return json.dumps({"version":appVersion,"response":response},indent=2,sort_keys=True)


def request_handler(session, user, request):
	requestType = request['type']
	
	if requestType == "LaunchRequest":
		return launch_request(session, user, request)
	elif requestType == "IntentRequest":
		return intent_request(session, user, request)


def launch_request(session, user, request):
	if not nest.isValidUser(user.getUserId()):
		output_speech = "Current user is not a valid nest user. Please look at the Echo app for help"
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "Nest Control - Setting Nest Temp"
		card_content = "Current user is not a valid nest user. Please authenticate user with userId: " + user.getUserId() + " to Nest as instructed in the README"

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}


		return response
	else:
		output_speech = "Welcome to Nest Control App. Please say a command."
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "Nest Control - Welcome"
		card_content = "Welcome to Nest Control App. Please say a command."

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':False}

		return response

def intent_request(session, user, request):
	print "intent_request"

	if not nest.isValidUser(user.getUserId()):
		output_speech = "Current user is not a valid nest user. Please look at the Echo app for help"
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "Nest Control - Setting Nest Temp"
		card_content = "Current user is not a valid nest user. Please authenticate user with userId: " + user.getUserId() + " to Nest as instructed in the README"

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}


		return response

	else:

		if request['intent']['name'] ==  "NestSetTempIntent":
			nestTempValue = request['intent']['slots']['temp']['value']
			output_speech = "Setting Nest to " + str(nestTempValue) + " degrees fahrenheit"
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "Nest Control - Setting Nest Temp"
			card_content = "Telling Nest to set to " + str(nestTempValue) + " degrees fahrenheit."

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

			if int(nestTempValue) <= 90:
				nest.setTemperatureTargetAll(user.getUserId(),int(nestTempValue))

			return response

		elif request['intent']['name'] ==  "NestCoolDownIntent":
			setTemp = nest.setTurnDownTemperatureAll(user.getUserId())
			output_speech = "Turning down the Nest"
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "Nest Control - Setting Nest Temp"
			card_content = "Telling Nest to set to " + "str(setTemp+2)" + " degrees fahrenheit."

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

			

			return response

		elif request['intent']['name'] ==  "NestWarmUpIntent":
			setTemp = nest.setTurnUpTemperatureAll(user.getUserId())
			output_speech = "Turning up the Nest"
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "Nest Control - Setting Nest Temp"
			card_content = "Telling Nest to set to " + "str(setTemp+2)" + " degrees fahrenheit."

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

			

			return response
		
		elif request['intent']['name'] ==  "HelpIntent":
			output_speech = "This is the Nest control app. You can tell me to set temperature to 74 degrees fahrenheit. You can also say that you are too hot or too cold and I will adjust the temperature by two degrees."
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "Nest Control - Help"
			card_content = "This is the Nest control app. You can tell me to set temperature to 74 degrees. You can also say that you are too hot or too cold and I will adjust the temperature by two degrees."

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':False}


			return response

		else:
			return launch_request(session, user, request) ##Just do the same thing as launch request





class Session:
	def __init__(self,sessionData):
		self.sessionId = sessionData['sessionId']


	def getSessionID(self):
		return self.sessionId

class User:
	def __init__(self,userId):
		self.userId = userId
		self.settings = {}

	def getUserId(self):
		return self.userId

class DataStore:
	def __init__(self):
		self.sessions = {}
		self.users = {}

	def getSession(self,session):
		if session['new'] is True or session['sessionId'] not in self.sessions:
			self.sessions[session['sessionId']] = Session(session)

		return self.sessions[session['sessionId']]

	def getUser(self,session):
		userId = session['user']['userId']
		if userId not in self.users:
			self.users[userId] = User(userId)

		return self.users[userId]

