import pandas as pd
import re
from datetime import datetime
import networkx
from collections import Counter, defaultdict
from utils.asimov import Asimov
import nltk
from nltk.corpus import stopwords

class Analyse(Asimov):
    def __init__(self) -> None:
        super().__init__()
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))

    def count_words(self): 
        word_counts = Counter()
        for book in self.clean_tokens():
            for tokens in book.values():
                word_counts.update(Counter(token for token in tokens if token not in self.stop_words))
        return word_counts

    def count_entities_per_chapter(self):
        entity_counts = []
        for book in self.entities():
            temp = {}
            for chapter, ents in book.items():
                temp[chapter] = len(ents)
            entity_counts.append(temp)
        return entity_counts
    
    def count_character_instances(self):
        counts = []
        for book in self.trilogy():
            temp = {}
            for chapter, text in book.items():
                char_temp = {}
                for character, aliases in self.characters.items():
                    for alias in aliases:
                        char_temp[character] += len(re.findall(r'\b' + re.escape(alias) + r'\b', text, re.IGNORECASE))
                temp[chapter] = char_temp
            counts.append(temp)
        return counts
    

    @staticmethod
    def get_characters(entities):
        characters = []
        for person in entities['PERSON']:
            if person not in characters:
                characters.append(person)

    @staticmethod
    def get_locations(entities):
        locations = []
        location_entities = ['GPE', 'LOC']
        for loc_type in location_entities:
            for location in entities[loc_type]:
                if location not in locations:
                    locations.append(location)
        return locations
    
    @staticmethod
    def determine_relationship_types(sentiment_relationships):
        relationship_types = []
        for subject, obj, sentiment in sentiment_relationships:
            if sentiment == 0:
                relationship = 'negative'
            elif sentiment == 1:
                relationship = 'neutral'
            else:
                relationship = 'positive'
            
            if subject and obj:
                relationship_types.append((subject, obj, relationship))
            elif subject:
                relationship_types.append((subject, 'Unknown', relationship))
            elif obj:
                relationship_types.append(('Unknown', obj, relationship))
        
        return relationship_types


