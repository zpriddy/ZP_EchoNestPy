import json
import requests
import pickle
import nestpy_settings as settings
import os.path

loadSettings = True
picklefile = 'nest_settings.pickle'


def nestDataStoreInit():
	global nestData 
	if loadSettings and os.path.isfile(picklefile):
		nestData = pickle.load(open(picklefile,'rb'))
	else:
		nestData = NestDataStore()



def nestAuth(userId):
	global nestData
	nestData.addUser(userId,NestUser(userId))
	auth_uri = settings.nest_auth_uri_1.replace('STATE',userId)
	return auth_uri

def nestToken(userId,authCode):
	global nestData
	currentUser = nestData.getUser(userId)

	print "NEST TOKEN"

	token_uri = settings.nest_auth_uri_2.replace('AUTHORIZATION_CODE',authCode)
	usertoken = requests.post(token_uri).json()['access_token']

	currentUser.setToken(usertoken)

	getStructures(userId)
	getThermostats(userId)


	pickle.dump(nestData,open(picklefile,"wb"))

	return True

def getStructures(userId):
	global nestData
	currentUser = nestData.getUser(userId)
	structures_uri = "https://developer-api.nest.com/structures?auth=" + currentUser.getToken()

	structures_raw = requests.get(structures_uri).json()
	currentUser.structures = {}
	for key in structures_raw.keys():
		currentUser.structures[structures_raw[key]['name']] = {"id":key,"thermostats":structures_raw[key]['thermostats']}
	print currentUser.structures

def getThermostats(userId):
	global nestData
	currentUser = nestData.getUser(userId)
	thermostats_uri = "https://developer-api.nest.com/devices/thermostats?auth=" + currentUser.getToken()

	thermostats_raw = requests.get(thermostats_uri).json()
	currentUser.thermostats = {}
	for key in thermostats_raw.keys():
		currentUser.thermostats[thermostats_raw[key]['name']] = {"id":key,"status":thermostats_raw[key]}
	print currentUser.thermostats

def setTemperatureTargetAll(userId,temp):
	print "SET TEMP"
	global nestData
	currentUser = nestData.getUser(userId)
	thermostats = currentUser.getThermostatIds()
	token = currentUser.getToken()

	command = {"target_temperature_f":int(temp)}

	commandSucessfull = True


	for device in thermostats:
		print "Device:" + device
		command_uri = 'https://developer-api.nest.com/devices/thermostats/' + device + "?auth=" + token
		print command_uri
		response = requests.put(url=command_uri, data=command, json=command)
		print response
		print response.text
		if response.status_code != 200:
			commandSucessfull = False

	return commandSucessfull

def setTurnDownTemperatureAll(userId):
	print "Turn Down Temp"
	global nestData
	currentUser = nestData.getUser(userId)
	thermostats = currentUser.getThermostats()
	token = currentUser.getToken()

	commandSucessfull = True

	#setTemperatureTargetAll(userId, int(getAvgTargetTemp(userId))-2)
	
	getThermostats(userId)
	for device in thermostats:
		currentTemp = thermostats[device]['status']['target_temperature_f']
		deviceId = thermostats[device]['id']
		command = {"target_temperature_f":int(currentTemp)-2}
		command_uri = 'https://developer-api.nest.com/devices/thermostats/' + deviceId + "?auth=" + token
		response = requests.put(url=command_uri, data=command, json=command)
		if response.status_code != 200:
			commandSucessfull = False

	return commandSucessfull


def setTurnUpTemperatureAll(userId):
	print "Turn Up Temp"
	global nestData
	currentUser = nestData.getUser(userId)
	thermostats = currentUser.getThermostats()
	token = currentUser.getToken()

	commandSucessfull = True


	#setTemperatureTargetAll(userId, int(getAvgTargetTemp(userId))+2)
	
	getThermostats(userId)
	for device in thermostats:
		currentTemp = thermostats[device]['status']['target_temperature_f']
		deviceId = thermostats[device]['id']
		command = {"target_temperature_f":int(currentTemp)+2}
		command_uri = 'https://developer-api.nest.com/devices/thermostats/' + deviceId + "?auth=" + token
		response = requests.put(url=command_uri, data=command, json=command)
		if response.status_code != 200:
			commandSucessfull = False
	
	return commandSucessfull
	


def setModeAll(userId,mode):
	print "SET Away"
	global nestData
	currentUser = nestData.getUser(userId)
	structures = currentUser.getStructureIds()
	token = currentUser.getToken()

	command = {"away":mode}

	commandSucessfull = True


	for structure in structures:
		command_uri = 'https://developer-api.nest.com/structures/' + structure + "?auth=" + token
		response = requests.put(url=command_uri, data=command, json=command)
		if response.status_code != 200:
			commandSucessfull = False

	return commandSucessfull
	

def getAvgTemp(userId):
	global nestData
	currentUser = nestData.getUser(userId)
	getThermostats(userId)
	thermostats = currentUser.getThermostats()
	
	temps = [a['status']['ambient_temperature_f'] for a in thermostats.values()]
	avgTemp = sum(temps)/len(temps)

	return avgTemp

def getAvgTargetTemp(userId):
	global nestData
	currentUser = nestData.getUser(userId)
	getThermostats(userId)
	thermostats = currentUser.getThermostats()
	
	temps = [a['status']['target_temperature_f'] for a in thermostats.values()]
	avgTemp = sum(temps)/len(temps)

	return avgTemp

def isValidUser(userId):
	global nestData

	return nestData.isValidUser(userId)







class NestUser: 
	def __init__(self,userId):
		self.userId = userId
		self.token = None
		self.devices = {}
		self.structures = {}
		self.thermostats = {}
		self.authed = False

	def setToken(self,token):
		self.token = token
		self.authed = True

	def getToken(self):
		return self.token

	def getThermostats(self):
		return self.thermostats

	def getThermostatIds(self):
		ids = [a['id'] for a in self.thermostats.values()]
		return ids

	def getStructureIds(self):
		ids = [a['id'] for a in self.structures.values()]
		return ids

class NestDataStore:
	def __init__(self):
		self.nestUsers = {}

	def addUser(self, userId, nestUser):
		if userId not in self.nestUsers:
			self.nestUsers[userId] = nestUser

	def getUser(self, userId):
		if userId not in self.nestUsers:
			self.addUser(userId,NestUser(userId))

		return self.nestUsers[userId]

	def isValidUser(self,userId):
		if userId in self.nestUsers:
			return True
		else:
			return False

		
