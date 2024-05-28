import pandas as pd
from datetime import datetime

class Analyse:
    def __init__(self, entities, relationships, sentiments) -> None:
        self.entities = entities
        self.relationships = relationships
        self.sentiments = sentiments

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
    def filter_key_events(relationships, central_characters):
        key_events = []
        for rel in relationships:
            entities, governor, relation, dependent = rel
            involved_entities = {ent[0] for ent in entities}
            if central_characters.intersection(involved_entities):
                key_events.append((entities, governor, relation, dependent))
        return key_events

