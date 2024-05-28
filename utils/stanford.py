import stanza
from collections import defaultdict
from tqdm import tqdm


class Stanford:
    def __init__(self) -> None:
        # Download necessary Stanford NER data
        stanza.download('en')
        # Initialize pipelines
        self.stanza_pipeline = stanza.Pipeline('en', processors='tokenize,lemma,pos,mwt,ner,sentiment,depparse', use_gpu=True)
        self.entities = []
        self.events = []
        self.interactions = []
        self.sentiments = []

    
    def get_info_per_book_per_chapter(self, books):
        for book in books:
            entities_temp = {}
            events_temp = {}
            interactions_temp = {}
            sentiments_temp = {}
            for chapter, text in book.items():
                if text:
                    (ent, event, inter, sent) = self.extract_information(text)
                    if (ent not in entities_temp[chapter] or event not in events_temp[chapter] or inter in interactions_temp[chapter]):
                        entities_temp[chapter] = ent 
                        events_temp[chapter] = event
                        interactions_temp[chapter] = inter
                    sentiments_temp[chapter] = sent
            self.entities.append(entities_temp)
            self.events.append(events_temp)
            self.interactions.append(interactions_temp)
            self.sentiments.append(sentiments_temp)

    
    def extract_information(self, text):
        doc = self.stanza_pipeline(text)
        entities = self.extract_named_entities(doc)
        events, interactions = self.extract_relationships(doc)
        sentiments = self.sentiment_analysis(doc)
        return entities, events, interactions, sentiments

    @staticmethod
    def extract_named_entities(doc):
        entities = defaultdict(list)
        for sentence in tqdm(doc.sentences, desc='Extracting Named Entities'):
            for ent in sentence.ents:
                if ent.text not in entities[ent.type]:
                    entities[ent.type].append(ent.text)
        return entities

    @staticmethod
    def extract_relationships(doc):
        events = []
        interactions = []
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.upos == 'VERB':
                    subject = None
                    objects = []
                    for dep in sentence.words:
                        if dep.head == word.id:
                            if dep.deprel in ['nsubj', 'nsubj:pass']:
                                subject = dep.text
                            elif dep.deprel in ['obj', 'iobj']:
                                objects.append(dep.text)
                    if subject and objects:
                        for obj in objects:
                            events.append(f"{subject} {word.text} {obj}")
                            interactions.append((subject, obj))
        
        return events, interactions

    @staticmethod
    def sentiment_analysis(doc):
        sentiments = [sentence.sentiment for sentence in tqdm(doc.sentences, desc='Analyzing Sentiment')]
        return sentiments
