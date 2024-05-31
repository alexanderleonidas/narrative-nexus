from utils.stanford import Stanford
from utils.helper import Helper
from utils.asimov import Asimov

helper = Helper()
asimov = Asimov()
stanford = Stanford()

try:
    trilogy = helper.load_data('data/processed_asimov.pkl')
except Exception:
    print('No such file')

def get_named_entities(trilogy):
    entites = []
    for book in trilogy:
        temp = {}
        for chapter, text in book.items():
            document = stanford.convert_to_document(text)
            temp[chapter] = stanford.extract_named_entities(document)
        entites.append(temp)
    
    helper.save_data(entites, 'data/entities.pkl')

def get_tokens():
    tokens=[]
    for book in trilogy:
        temp = {}
        for chapter, text in book.items():
            doc = stanford.convert_to_document(text)
            temp[chapter] = stanford.get_tokens(doc)
        tokens.append(temp)

    helper.save_data(tokens, 'data/tokenized_trilogy.pkl')