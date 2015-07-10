import os
import echopy_app
import echopy_doc
import echopy_nest as myApp
import nestpy_app
import nestpy_lib as nest
import nestpy_settings as settings
from flask import Flask, render_template, Response, send_from_directory, request, current_app, redirect, jsonify, json


app = Flask(__name__)


@app.route("/alexa/")
def main():
	return echopy_doc.main_page


@app.route("/alexa/EchoPyAPI",methods = ['GET','POST'])
def apicalls():
	if request.method == 'POST':
		data = request.get_json()
		print "POST"
		sessionId = myApp.data_handler(data)
		return sessionId + "\n"

@app.route("/alexa/auth/<path:path>",methods = ['GET'])
def auth(path):

	auth_uri = nest.nestAuth(path)
	return redirect(auth_uri)

@app.route("/alexa/oauth2",methods = ['GET'])
def authcode():
	user = request.args.get('state')
	code = request.args.get('code')

	if nest.nestToken(user,code):

		print nest.nestData.getUser(user).getToken()

	return redirect("/alexa")




def run_echopy_app():
	import SocketServer
	#SocketServer.BaseServer.handle_error = close_stream
	SocketServer.ThreadingTCPServer.allow_reuse_address = True
	echopy_app.run(app)


if __name__ == "__main__":
	nest.nestDataStoreInit()
	myApp.data_init()
	run_echopy_app()
