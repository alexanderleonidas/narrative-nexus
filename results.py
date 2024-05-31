from utils.helper import Helper
from utils.analyse import Analyse

helper = Helper()

entities = helper.load_data('data/03/NER_results.pkl')
events = helper.load_data('data/03/events.pkl')
interactions = helper.load_data('data/03/interactions.pkl')
sentiments = helper.load_data('data/03/sentiment_results.pkl')

#analyse = Analyse(entities, events, interactions, sentiments)


people = entities['DATE']
print(people)