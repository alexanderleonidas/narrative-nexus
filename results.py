from utils.helper import Helper
from utils.analyse import Analyse

helper = Helper()

entities = helper.load_data('data/NER_results.pkl')
relationships = helper.load_data('data/relationships_results.pkl')
sentiments = helper.load_data('data/sentiment_results.pkl')

analyse = Analyse(entities, relationships, sentiments)

print(relationships)

