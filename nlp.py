from utils.stanford import Stanford
from utils.helper import Helper
from utils.asimov import Asimov
from utils.preprocess import Preprocess
import os.path

helper = Helper()
asimov = Asimov()
stanford = Stanford()


tokens = []
entities = []
events = []
interactions = []
sentiments = []

def get_clean_tokens():
    clean_tokens = []
    for book in asimov.tokens():
        temp = {}
        for chapter, tokens in book.items():
            l = []
            for token in tokens:
                clean = Preprocess().clean_text(token)
                if clean != '':
                    l.append(clean)
            temp[chapter] = l
        clean_tokens.append(temp)

    Helper().save_data(clean_tokens, 'data/tokenized_asmimov_clean.pkl')

def get_information(tok=True,ent=False,rel=False,sent=False):
    for book in asimov.clean_trilogy():
        tokens_temp = {}
        entities_temp = {}
        events_temp = {}
        interactions_temp = {}
        sentiments_temp = {}

        for chapter, text in book.items():
            if text:
                stanford.convert_to_document(text)
                tokens_temp[chapter] = stanford.get_tokens() if tok else None
                entities_temp[chapter] = stanford.extract_named_entities() if ent else None
                events_temp[chapter], interactions_temp[chapter] = stanford.extract_person_relationships() if rel else None
                sentiments_temp[chapter] = stanford.extract_sentiment() if sent else None
        
        tokens.append(tokens_temp)
        entities.append(entities_temp)
        events.append(events_temp)
        interactions.append(interactions_temp)
        sentiments.append(sentiments_temp)

    if not os.path.isfile('data/entities.pkl') and ent:
        Helper().save_data(entities, 'data/entities.pkl')

    if not os.path.isfile('data/tokenized_clean_asimov.pkl') and tok:
        Helper().save_data(tokens, 'data/tokenized_clean_asimov.pkl')

if __name__ == '__main__':
    get_information()