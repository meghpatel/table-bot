from flask import Flask, render_template, url_for, request, jsonify, after_this_request, make_response
from werkzeug.utils import secure_filename
import pandas as pd
import os
import csv
import json 
from rivia import Rivia

app = Flask(__name__) 

app.config['UPLOAD_FOLDER'] = 'data/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv','tsv'}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

current_file = 'data/output.tsv'

rivia = None


# @app.before_first_request
def load_func():
	global rivia
	rivia = Rivia('table')
	rivia.what()
	print ('Loaded')

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


# def check_name():

# 	#open the file


# @app.before_first_request(load_func())	  

@app.route('/') 
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
			
			if f.filename.rsplit('.', 1)[1].lower() in ['csv', 'tsv', 'db']:
				rivia.type = 'table'
			
			rivia.process_file(path)

			df = pd.read_csv(path)
			print (df.shape)
			ans = df.to_html(bold_rows=True,classes="table table-hover thead-light table-striped")
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

	result = rivia.rivia_predict(req['query'])
	print(result["logical_form"][0])

	ans = rivia.correct_answer(result['answer'])

	# reply = {"answer":ans}

	res = make_response(jsonify(ans), 200)
	# print (answer())
	return res

if __name__ == '__main__': 
	load_func()
	app.run(debug=True) 