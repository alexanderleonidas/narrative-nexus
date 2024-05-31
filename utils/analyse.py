import pandas as pd
from datetime import datetime
import networkx
import matplotlib.pyplot as plt
from collections import Counter

class Analyse:
    def __init__(self, entities, events, interactions, sentiments) -> None:
        self.entities = entities
        self.events = events
        self.interactions = interactions
        self.sentiments = sentiments

    @staticmethod
    def count_entities_per_chapter(entities):
        entity_counts = []
        for book in entities:
            temp = {}
            for chapter, ents in book:
                temp[chapter] = len(ents)
            entity_counts.append(temp)
        return entity_counts

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


