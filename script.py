from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp_rc.predictors.reading_comprehension import ReadingComprehensionPredictor
from allennlp_semparse.predictors.wikitables_parser import WikiTablesParserPredictor
from allennlp_semparse.models.wikitables.wikitables_erm_semantic_parser import WikiTablesErmSemanticParser
import pytest
import spacy
from allennlp.common.testing import AllenNlpTestCase
from allennlp_hub import pretrained
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
import pandas as pd


# last_line = []
# with open('data/output.txt', 'r') as f:
# 	lines = f.read().splitlines()
# 	last_line = lines[:-1]
# 	print ('.'.join(last_line))
# ans = '.'.join(last_line)
# with open('data/final_output.txt', 'w+') as f:
# 	f.write(ans)

# fd=open("data/output.txt","r")
# d=fd.read()
# fd.close()
# m=d.split("\n")
# s="\n".join(m[:-1])
# fd=open("data/final_output.txt","w+")
# for i in range(len(s)):
#     fd.write(s[i])
# fd.close()

archive = load_archive("model/wikitables-model-2020.02.10.tar.gz")
predictor = Predictor.from_archive(archive, 'wikitables-parser')
with open('data/final_output.txt','r') as f:
	table = f.read()
# print (query)
# print (table)
question = "Which country have death greater than 5000?"
data = {
  "table": table,
  "question": question
}

result = predictor.predict_json(data)
print(result["answer"])
# print(result["logical_form"][0])

temp_answer = result['answer']
print (type(temp_answer))

print (type([1,2]))

if type([1,2]) is list:
	print ('yes')

if type(temp_answer) is list:
	df = pd.read_table('data/final_output.txt','\t')
	types = dict(df.dtypes)

	checks = []
	for key, value in types.items():
		if (value == 'object'):
			checks.append(key)

	thershold = 50
	final_answer = []

	for answer in temp_answer:
		match = {}
		# print (answer)
		for check in checks:
			for index, row in df.iterrows(): 
				# print (row[check]) 
				if process.extractOne(answer,[row[check]])[1] > 50:
					# print (row[check])
					match[row[check]] = process.extractOne(answer,[row[check]])[1]

		# print (match)
		max_val = 0
		max_key = ''
		for key in match.keys():
			if match[key]>max_val:
				max_val = match[key]
				max_key = key
		# print(max_key, max_val)		# pass
		final_answer.append(max_key)
		print (final_answer)

# print (final_answer)
# reply = {'answer':result['answer']}
# print (type(jsonify(reply)))
# fd=open("file.txt","r")
# d=fd.read()
# fd.close()
# m=d.split("\n")
# s="\n".join(m[:-1])
# fd=open("file.txt","w+")
# for i in range(len(s)):
# 	fd.write(s[i])
# fd.close()


query = 'united_states'
choices = ['United States']
   
# Get a list of matches ordered by score, default limit to 5 
print (process.extractOne(query, choices)) 
   
# If we want only the top one 
# print (process.extractOne(query, choices) )