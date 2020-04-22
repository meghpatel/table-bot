from flask import Flask, render_template, url_for, request, jsonify, after_this_request
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__) 
  
@app.route('/') 
def home():
	return render_template("index.html")

@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
	@after_this_request
	def add_header(response):
		response.headers['Access-Control-Allow-Origin'] = '*'
		return response
	df = pd.read_csv('data/train.csv')
	print (df.shape)
	ans = df.to_html(bold_rows=True)
	resp = {"ans":ans}
	return jsonify(resp)

if __name__ == '__main__': 
	app.run(debug=True) 