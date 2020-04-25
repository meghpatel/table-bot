from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp_rc.predictors.reading_comprehension import ReadingComprehensionPredictor
from allennlp_semparse.predictors.wikitables_parser import WikiTablesParserPredictor
from allennlp_semparse.models.wikitables.wikitables_erm_semantic_parser import WikiTablesErmSemanticParser
import pytest
import spacy
from allennlp.common.testing import AllenNlpTestCase
from allennlp_hub import pretrained

# archive_file =  "https://storage.googleapis.com/allennlp-public-models/bidaf-model-2020.02.10-charpad.tar.gz"
# archive = load_archive(archive_file)
# bidaf = Predictor.from_archive(archive, "reading-comprehension")

# data = { 
#   "question": "Who stars in The Matrix?", 
#   "passage": 'The Matrix is a 1999 science fiction action film written and directed by The Wachowskis, starring Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, and Joe Pantoliano. It depicts a dystopian future in which reality as perceived by most humans is actually a simulated reality called "the Matrix", created by sentient machines to subdue the human population, while their bodies\' heat and electrical activity are used as an energy source. Computer programmer "Neo" learns this truth and is drawn into a rebellion against the machines, which involves other people who have been freed from the "dream world.'
# }

# result = bidaf.predict_json(data)
# print(result['best_span_str'])

archive = load_archive("https://storage.googleapis.com/allennlp-public-models/wikitables-model-2020.02.10.tar.gz")
# predictor = Predictor.from_archive(archive, 'wikitables-parser')

# data = {
#   "table": "#\tEvent Year\tSeason\tFlag bearer\n7\t2012\tSummer\tEle Opeloge\n6\t2008\tSummer\tEle Opeloge\n5\t2004\tSummer\tUati Maposua\n4\t2000\tSummer\tPauga Lalau\n3\t1996\tSummer\tBob Gasio\n2\t1988\tSummer\tHenry Smith\n1\t1984\tSummer\tApelu Ioane",
#   "question": "How many years were held in summer?"
# }

# result = predictor.predict_json(data)
# print(result["answer"])
# print(result["logical_form"])

predictor = pretrained.wikitables_parser_dasigi_2019()
table = """#	Event Year	Season	Flag bearer
7	2012	Summer	Ele Opeloge
6	2008	Summer	Ele Opeloge
5	2004	Summer	Uati Maposua
4	2000	Summer	Pauga Lalau
3	1996	Summer	Bob Gasio
2	1988	Summer	Henry Smith
1	1984	Summer	Apelu Ioane"""

question = "Who is the flag bearer in 1996??"
result = predictor.predict_json({"table": table, "question": question})

print(result["answer"])
print(result["logical_form"][0])