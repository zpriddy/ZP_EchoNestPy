import os
import nestpy_app
import nestpy_lib as nest
import nestpy_settings as settings

import requests

from flask import Flask, render_template, Response, send_from_directory, request, current_app, redirect, jsonify, json


app = Flask(__name__)


@app.route("/")
def main():
	return "Web Interface for NestPy"


@app.route("/auth/<path:path>",methods = ['GET'])
def auth(path):

	auth_uri = nest.nestAuth(path)
	return redirect(auth_uri)

@app.route("/oauth2",methods = ['GET'])
def authcode():
	user = request.args.get('state')
	code = request.args.get('code')

	if nest.nestToken(user,code):

		print nest.nestData.getUser(user).getToken()

	return redirect("/")

@app.route("/users")
def listUsers():
	return str(nest.nestData.nestUsers.keys())

@app.route("/structures/<path:path>")
def listStructures(path):
	nest.getStructures(path)
	nest.getThermostats(path)
	return redirect("/")

@app.route("/set/<path:user>/<path:temp>")
def setTemp(user,temp):
	nest.setTemperatureTargetAll(user,temp)
	return redirect("/")

@app.route("/mode/<path:user>/<path:mode>")
def setMode(user,mode):
	nest.setModeAll(user,mode)
	return redirect("/")








def run_nestpy_app():
	import SocketServer
	#SocketServer.BaseServer.handle_error = close_stream
	SocketServer.ThreadingTCPServer.allow_reuse_address = True
	nestpy_app.run(app)


if __name__ == "__main__":
	nest.nestDataStoreInit()
	run_nestpy_app()
