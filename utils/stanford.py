import stanza
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
from tqdm import tqdm

# Download the stop words


class Stanford:
    def __init__(self) -> None:
        # Download necessary Stanford NER data
        stanza.download('en')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
        # Initialize pipelines
        self.stanza_pipeline = stanza.Pipeline('en', processors='tokenize,lemma,pos,mwt,ner,sentiment,depparse', package={"ner": ["conll03"]}, use_gpu=True)
        self.entities = []
        self.events = []
        self.interactions = []
        self.sentiments = []
    
    def convert_to_document(self, text):
        self.doc = self.stanza_pipeline(text)

    @staticmethod
    def get_tokens(doc: stanza.Document):
        return [token.text for sentence in doc.sentences for token in sentence.tokens]
    
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

    def extract_information(self, doc: stanza.Document):
        entities = self.extract_named_entities(doc)
        events, interactions = self.extract_relationships(doc)
        sentiments = self.sentiment_analysis(doc)
        return entities, events, interactions, sentiments

    @staticmethod
    def sentiment_analysis(doc: stanza.Document):
        sentiments = [sentence.sentiment for sentence in tqdm(doc.sentences, desc='Analyzing Sentiment')]
        return sentiments

    @staticmethod
    def extract_named_entities(doc: stanza.Document):
        # entities = defaultdict(list)
        entities = []
        for sentence in tqdm(doc.sentences, desc='Extracting Named Entities'):
            for token in sentence.tokens:
                if token.ner != "O":
                    # entities[ent.type].append(ent.text)
                    entities.append((token.text, token.ner))
        return entities
   

    @staticmethod
    def extract_relationships(doc: stanza.Document):
        events = []
        interactions = []
        entities = defaultdict(list)
        
        # Extract named entities first
        for sentence in doc.sentences:
            for ent in sentence.ents:
                entities[ent.text].append((ent.type, ent.start_char, ent.end_char))

        for sentence in tqdm(doc.sentences, desc='Extracting relationships'):
            named_entities_in_sentence = {ent.text for ent in sentence.ents}
            for word in sentence.words:
                if word.upos == 'VERB':
                    subject = None
                    objects = []
                    for dep in sentence.words:
                        if dep.head == word.id:
                            if dep.deprel in ['nsubj', 'nsubj:pass'] and dep.text in named_entities_in_sentence:
                                subject = dep.text
                            elif dep.deprel in ['obj', 'iobj'] and dep.text in named_entities_in_sentence:
                                objects.append(dep.text)
                    if subject and objects:
                        for obj in objects:
                            events.append(f"{subject} {word.text} {obj}")
                            interactions.append((subject, obj))
                    elif subject:
                        events.append(f"{subject} {word.text}")
                    elif objects:
                        for obj in objects:
                            events.append(f"{word.text} {obj}")

        return events, interactions
    
    def extract_person_relationships(self, doc: stanza.Document):
        person_entities = defaultdict(list)
        relationships = []
        sentiment_relationships = []

        # Extract named entities classified as 'PERSON'
        for sentence in doc.sentences:
            for ent in sentence.ents:
                if ent.type == 'PERSON':
                    person_entities[ent.text].append((ent.start_char, ent.end_char))

        for sentence in tqdm(doc.sentences, desc='Extracting relationships between PERSON entities'):
            persons_in_sentence = {ent.text for ent in sentence.ents if ent.type == 'PERSON'}
            sentiment = sentence.sentiment
            negation = any(word.text.lower() in ['not', 'no', 'never'] for word in sentence.words)
            
            for word in sentence.words:
                if word.upos == 'VERB':
                    subject = None
                    objects = []
                    for dep in sentence.words:
                        if dep.head == word.id:
                            if dep.deprel in ['nsubj', 'nsubj:pass']:
                                if dep.text in persons_in_sentence:
                                    subject = dep.text
                                else:
                                    subject = self.resolve_anaphora(dep, sentence, persons_in_sentence)
                            elif dep.deprel in ['obj', 'iobj']:
                                if dep.text in persons_in_sentence:
                                    objects.append(dep.text)
                                else:
                                    resolved_object = self.resolve_anaphora(dep, sentence, persons_in_sentence)
                                    if resolved_object:
                                        objects.append(resolved_object)
                    if subject and objects:
                        for obj in objects:
                            relationships.append(f"{subject} {word.text} {obj}")
                            sentiment_relationships.append((subject, obj, sentiment, negation))
                    elif subject:
                        relationships.append(f"{subject} {word.text}")
                        sentiment_relationships.append((subject, None, sentiment, negation))
                    elif objects:
                        for obj in objects:
                            relationships.append(f"{word.text} {obj}")
                            sentiment_relationships.append((None, obj, sentiment, negation))
        
        return relationships, sentiment_relationships

    @staticmethod
    def resolve_anaphora(dep, sentence, persons_in_sentence):
        # Basic heuristic for anaphora resolution: look for the closest preceding named entity
        for word in reversed(sentence.words[:dep.id]):
            if word.text in persons_in_sentence:
                return word.text
        return None
