from flask import Flask, render_template, url_for, request, jsonify, after_this_request, make_response
from werkzeug.utils import secure_filename
import pandas as pd
import os
import csv
import json 
from rivia import Rivia
import webbrowser
from threading import Timer
import speech_recognition as sr
from gtts import gTTS 
import regex as re

app = Flask(__name__) 

app.config['UPLOAD_FOLDER'] = 'data/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv','tsv'}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
RECORDED_FILES_PATH = 'static/audio/'

current_file = 'data/output.tsv'
app = Flask(__name__, static_folder='static')

rivia = None
typefile = str()

# @app.before_first_request
def load_func():
	global rivia
	rivia = Rivia()
	rivia.what()
	# rivia = Rivia('table')
	# rivia.what()
	# print ('Loaded')

def allowed_file(filename):
	return '.' in filename and \
 		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def answer(query):
	#Loading the model
	# archive = load_archive("model/wikitables-model-2020.02.10.tar.gz")
	# predictor = Predictor.from_archive(archive, 'wikitables-parser')

	#Reading the Data
	# with open('data/final_output.txt','r') as f:
	# 	table = f.read()
		

	# question = query
	# data = {
	#   "table": table,
	#   "question": question
	# }

	# result = predictor.predict_json(data)
	# print(result["answer"])
	# print(result["logical_form"][0])

	# reply = {"answer":result['answer']}
	# # print (type(jsonify(reply)))
	# print (str(reply))
	# print (type(result['answer']))
	return str(reply)

def compute_results(question):
	result,typefile = rivia.rivia_predict(question)
	print(typefile)
	if typefile == 'table':
		print(result["logical_form"][0])
		ans = rivia.correct_answer(result['answer'])
	else:
		print(result["best_span_str"])
		ans = result["best_span_str"]
	return ans


# def check_name():

# 	#open the file


# @app.before_first_request(load_func())	  
# @app.route('/')
# def index():
# 	return render_template('homepage.html')

@app.route('/home') 
def home():
	return render_template("index.html")

# @app.route('/getdata', methods=['GET', 'POST'])
# def getdata():
# 	@after_this_request
# 	def add_header(response):
# 		response.headers['Access-Control-Allow-Origin'] = '*'
# 		return response

# 	df = pd.read_csv('data/cases.csv')
# 	print (df.shape)
# 	ans = df.to_html(bold_rows=True,classes="table table-hover thead-light table-striped")
# 	resp = {"ans":ans}

# 	return jsonify(resp)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		f = request.files['table']
		if f and allowed_file(f.filename):
			path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
			f.save(path)
			extention = f.filename.rsplit('.', 1)[1].lower()
			if extention in ['csv', 'tsv', 'db']:
				print ('Table loaded')
				typefile = 'table'
			elif extention in ['txt']:
				print ('Passage loaded')
				typefile = 'passage'		
			rivia.process_file(path,typefile)
			
			if typefile == 'table':
				df = pd.read_csv(path)
				print (df.shape)
				ans = df.to_html(bold_rows=True,classes="table table-hover thead-light table-striped")
			else:
				f = open(path,'r+').read()
				ans = "<h4 style=\"margin-left:50px;margin-right:50px\">"+f+"</h4>"

			resp = {"ans":ans}
		else:
			resp = {"ans":"Out of format"}
		return jsonify(resp)
	else:
		return 'GETTTTT OUT'

@app.route('/getanswer', methods=['GET', 'POST'])
def getanswer():
	print ('Got another request')
	req = request.get_json()
	print(req)
	# reply = answer(req['query'])
	
	
	# reply = {"answer":ans}
	ans = compute_results(req['query'])
	res = make_response(jsonify(ans), 200)
	# print (answer())
	return res

@app.route('/audio')
def audio():
	return render_template("audio.html")

# @app.route('/wikiqa')
# def wikiqa():
# 	return render_template('wikiqa.html')
if __name__ == '__main__': 
@app.route('/speech', methods = ['POST', 'PUT', 'GET'])
def speech():
	if request.method == 'GET':
		print ("Request MEthod: "+str(s))
		return "Wrong Method"
	if request.method == 'POST':

		print ("In post")

		f = request.files['audio_data']
		print (f)
		path = os.path.join(RECORDED_FILES_PATH, secure_filename(f.filename))
		f.save(path)
		# f.save(secure_filename(f.filename))

		regex = re.compile(r'[0-9]')
		message_number = regex.findall(secure_filename(f.filename))[0]


		print ("Got the file.")

		r=sr.Recognizer() 
		file=sr.AudioFile(path)

		with file as source:
		   audio = r.record(source)
		#  Speech recognition using Google Speech Recognition
		try:
			recog = r.recognize_google(audio, language = 'en-US')
			# for testing purposes, we're just using the default API key
			# to use another API key, use r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")
			# instead of `r.recognize_google(audio)`` 

			print("You said: " + recog)
			query = recog

			answer = compute_results(query)
			print ("Answer",answer)
			print (type(answer))
			# i = 0
			path = "static/audio/answer_{}.mp3".format(message_number)
			response_path = "../" + path

			ans = {"query" : query,"path":response_path, "textres":answer, "status":"OK"}
			myobj = gTTS(text=str(answer), lang='en', slow=False)
			myobj.save(path) 
			
			res = json.dumps(ans)

		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			ans = {"query":"Sorry, I don't quite understand what you said.", "status":"NOT OK"}
			res = json.dumps(ans)


		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
			ans = {"query":"Sorry, We can't process your speech at this moment. Kindly use text input.", "status":"NOT OK"}
			res = json.dumps(ans)

		
		return res
	else:
		return "No method"

def open_browser():
	path = '/usr/bin/google-chrome %s --incognito'
	webbrowser.get(path).open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
	load_func()
	Timer(1, open_browser).start();
	app.run(debug=True) 