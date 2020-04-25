from flask import Flask, render_template, url_for, request, jsonify, after_this_request, make_response
from werkzeug.utils import secure_filename
import pandas as pd
import os
import csv
import json 

from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp_rc.predictors.reading_comprehension import ReadingComprehensionPredictor
from allennlp_semparse.predictors.wikitables_parser import WikiTablesParserPredictor
from allennlp_semparse.models.wikitables.wikitables_erm_semantic_parser import WikiTablesErmSemanticParser
import pytest
import spacy
from allennlp.common.testing import AllenNlpTestCase
from allennlp_hub import pretrained

app = Flask(__name__) 

app.config['UPLOAD_FOLDER'] = 'data/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv','tsv'}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

current_file = 'data/output.tsv'


# @app.before_first_request
def load_func():
	print ('Loaded')

def allowed_file(filename):
	return '.' in filename and \
 		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def answer(query):
	archive = load_archive("data/wikitables-model-2020.02.10.tar.gz")
	predictor = Predictor.from_archive(archive, 'wikitables-parser')
	with open('data/final_output.txt','r') as f:
		table = f.read()
	print (query)
	print (table)
	question = query
	data = {
	  "table": table,
	  "question": question
	}

	result = predictor.predict_json(data)
	print(result["answer"])
	print(result["logical_form"][0])

	reply = {"answer":result['answer']}
	# print (type(jsonify(reply)))
	print (str(reply))
	return str(reply)


# @app.before_first_request(load_func())	  

@app.route('/') 
def home():
	return render_template("index.html")

@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
	@after_this_request
	def add_header(response):
		response.headers['Access-Control-Allow-Origin'] = '*'
		return response

	df = pd.read_csv('data/cases.csv')
	print (df.shape)
	ans = df.to_html(bold_rows=True,classes="table table-hover thead-light table-striped")
	resp = {"ans":ans}

	return jsonify(resp)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
	# @after_this_request
	# def add_header(response):
	# 	response.headers['Access-Control-Allow-Origin'] = '*'
	# 	return response
	
	if request.method == 'POST':
		f = request.files['table']
		if f and allowed_file(f.filename):
			path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
			f.save(path)
			
			csv.writer(open("data/output.txt", 'w+'), delimiter='\t').writerows(csv.reader(open(path)))
			fd=open("data/output.txt","r")
			d=fd.read()
			fd.close()
			m=d.split("\n")
			s="\n".join(m[:-1])
			fd=open("data/final_output.txt","w+")
			for i in range(len(s)):
			    fd.write(s[i])
			fd.close()
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
	reply = answer(req['query'])

	res = make_response(jsonify(reply), 200)
	# print (answer())
	return res

if __name__ == '__main__': 
	load_func()
	app.run(debug=True) 