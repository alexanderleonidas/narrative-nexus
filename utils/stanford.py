import stanza
from collections import defaultdict
from tqdm import tqdm

# Download the stop words


class Stanford():
    def __init__(self) -> None:
        # Download necessary Stanford NER data
        stanza.download('en')
        # Initialize pipelines
        self.stanza_pipeline = stanza.Pipeline('en', processors='tokenize,lemma,pos,mwt,ner,sentiment,depparse', use_gpu=True)
    
    def convert_to_document(self, text):
        self.doc = self.stanza_pipeline(text)
    
    def get_tokens(self):
        return [token.text for sentence in self.doc.sentences for token in sentence.tokens]

    def extract_sentiment(self):
        sentiments = [sentence.sentiment for sentence in tqdm(self.doc.sentences, desc='Analyzing Sentiment')]
        return sentiments

    def extract_named_entities(self):
        # entities = defaultdict(list)
        entities = []
        for sentence in tqdm(self.doc.sentences, desc='Extracting Named Entities'):
            for token in sentence.tokens:
                if token.ner != "O":
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
    
    def extract_person_relationships(self):
        person_entities = defaultdict(list)
        relationships = []
        sentiment_relationships = []

        # Extract named entities classified as 'PERSON'
        for sentence in self.doc.sentences:
            for ent in sentence.ents:
                if ent.type == 'PERSON':
                    person_entities[ent.text].append((ent.start_char, ent.end_char))

        for sentence in tqdm(self.doc.sentences, desc='Extracting relationships between PERSON entities'):
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
