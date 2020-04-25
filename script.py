from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp_rc.predictors.reading_comprehension import ReadingComprehensionPredictor
from allennlp_semparse.predictors.wikitables_parser import WikiTablesParserPredictor
from allennlp_semparse.models.wikitables.wikitables_erm_semantic_parser import WikiTablesErmSemanticParser
import pytest
import spacy
from allennlp.common.testing import AllenNlpTestCase
from allennlp_hub import pretrained
# last_line = []
# with open('data/output.txt', 'r') as f:
# 	lines = f.read().splitlines()
# 	last_line = lines[:-1]
# 	print ('.'.join(last_line))
# ans = '.'.join(last_line)
# with open('data/final_output.txt', 'w+') as f:
# 	f.write(ans)

fd=open("data/output.txt","r")
d=fd.read()
fd.close()
m=d.split("\n")
s="\n".join(m[:-1])
fd=open("data/final_output.txt","w+")
for i in range(len(s)):
    fd.write(s[i])
fd.close()

# archive = load_archive("data/wikitables-model-2020.02.10.tar.gz")
# predictor = Predictor.from_archive(archive, 'wikitables-parser')
# with open('data/output.txt','r') as f:
# 	table = f.read()
# # print (query)
# print (table)
# question = "How many cases are there in India?"
# data = {
#   "table": table,
#   "question": question
# }

# result = predictor.predict_json(data)
# print(result["answer"])
# print(result["logical_form"][0])

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