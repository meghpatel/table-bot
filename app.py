from flask import Flask, render_template, url_for, request, jsonify, after_this_request
from werkzeug.utils import secure_filename
import pandas as pd
import os

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


# @app.before_first_request
def load_func():
	print ('Loaded')

def answer():
	archive = load_archive("data/wikitables-model-2020.02.10.tar.gz")
	predictor = Predictor.from_archive(archive, 'wikitables-parser')
	with open('data/cases.txt','r') as f:
		table = f.read()
	question = "How many cases are there in India?"
	data = {
	  "table": table,
	  "question": question
	}

	result = predictor.predict_json(data)
	print(result["answer"])
	print(result["logical_form"][0])


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
		# f.save(secure_filename(path))
		path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
		f.save(path)
		# with open(path,'ab') as a:
		# 	a.write(request.files['file'].read())
		return 'file uploaded successfully'
	else:
		return 'GETTTTT OUT'

@app.route('/test')
def test():
	answer()
	# print (answer())
	return 'done'

if __name__ == '__main__': 
	load_func()
	app.run(debug=True) 