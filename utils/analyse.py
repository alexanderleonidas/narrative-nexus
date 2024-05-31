import pandas as pd
import re
from datetime import datetime
import networkx
from collections import Counter, defaultdict

class Analyse:
    def __init__(self, entities) -> None:
        self.entities = entities

    def count_entities_per_chapter(self):
        entity_counts = []
        for book in self.entities:
            temp = {}
            for chapter, ents in book:
                temp[chapter] = len(ents)
            entity_counts.append(temp)
        return entity_counts
    
    def count_character_instances(self, characters, trilogy):
        counts = []
        for book in trilogy:
            temp = {}
            for chapter, text in book.items():
                char_temp = {}
                for character, aliases in characters.items():
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
    
    @staticmethod
    def count_most_common_words(tokenized_books, n=10):
        all_tokens = []
        for book in tokenized_books:
            for chapter, tokens in book.items():
                all_tokens.extend(tokens)
        
        word_counts = Counter(all_tokens)
        most_common_words = word_counts.most_common(n)
        
        return most_common_words


