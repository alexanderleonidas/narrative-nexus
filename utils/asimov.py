from utils.helper import Helper
import os.path

class Asimov:
    def __init__(self) -> None:
        self._path = "data/the_foundation.pdf"
        self._chapter_headers = [
                ['PART I THE PSYCHOHISTORIANS', 'PART II THE ENCYCLOPEDISTS','PART III THE MAYORS', 'PART IV THE TRADERS',
                 'PART V THE MERCHANT PRINCES'],
                ['PROLOGUE', '1. SEARCH FOR MAGICIANS', '2. THE MAGICIANS','3. THE DEAD HAND', '4. THE EMPEROR', '5. THE WAR BEGINS',
                 '6. THE FAVORITE', '7. BRIBERY', '8. TO TRANTOR', '9. ON TRANTOR', '10. THE WAR ENDS', '11. BRIDE AND GROOM',
                 '12. CAPTAIN AND MAYOR', '13. LIEUTENANT AND CLOWN', '14. THE MUTANT', '15. THE PSYCHOLOGIST', '16. CONFERENCE',
                 '17. THE VISI-SONOR', '18. FALL OF THE FOUNDATION', '19. START OF THE SEARCH', '20. CONSPIRATOR', '21. INTERLUDE IN SPACE',
                 '22. DEATH ON NEOTRANTOR', '23. THE RUINS OF TRANTOR', '24. CONVERT', '25. DEATH OF A PSYCHOLOGIST', '26. END OF THE SEARCH'],
                ['Prologue', '1 Two Men and the Mule', '2 Two Men without the Mule', '3 Two Men and a Peasant','4  Two Men and the Elders',
                 '5 One Man and the Mule', '6 One Man, the Mule – and Another', '7 Arcadia', '8 Seldon\'s Plan', '9 The Conspirators',
                 '10 Approaching Crisis', '11 Stowaway', '12 Lord', '13 Lady', '14  Anxiety', '15 Through the Grid', '16  Beginning of War',
                 '17 War', '18 Ghost of a World', '19 End of War', '20  "I Know ..."', '21 The Answer That Satisfied','22 The Answer That Was True']
                   ]
        
        self._chapter_headers_preprocess = [
                ['PART I THE PSYCHOHISTORIANS', 'PART II THE ENCYCLOPEDISTS','PART III THE MAYORS', 'PART IV THE TRADERS',
                 'PART V THE MERCHANT PRINCES', 'ABOUT THE AUTHOR'],
                ['PROLOGUE', '1. SEARCH FOR MAGICIANS', '2. THE MAGICIANS','3. THE DEAD HAND', '4. THE EMPEROR', '5. THE WAR BEGINS',
                 '6. THE FAVORITE', '7. BRIBERY', '8. TO TRANTOR', '9. ON TRANTOR', '10. THE WAR ENDS', '11. BRIDE AND GROOM',
                 '12. CAPTAIN AND MAYOR', '13. LIEUTENANT AND CLOWN', '14. THE MUTANT', '15. THE PSYCHOLOGIST', '16. CONFERENCE',
                 '17. THE VISI-SONOR', '18. FALL OF THE FOUNDATION', '19. START OF THE SEARCH', '20. CONSPIRATOR', '21. INTERLUDE IN SPACE',
                 '22. DEATH ON NEOTRANTOR', '23. THE RUINS OF TRANTOR', '24. CONVERT', '25. DEATH OF A PSYCHOLOGIST', '26. END OF THE SEARCH'],
                ['Prologue', '1 Two Men and the Mule', '2 Two Men without the Mule', '3 Two Men and a Peasant','4  Two Men and the Elders',
                 '5 One Man and the Mule', '6 One Man, the Mule – and Another', '7 Arcadia', '8 Seldon\'s Plan', '9 The Conspirators',
                 '10 Approaching Crisis', '11 Stowaway', '12 Lord', '13 Lady', '14  Anxiety', '15 Through the Grid', '16  Beginning of War',
                 '17 War', '18 Ghost of a World', '19 End of War', '20  "I Know ..."', '21 The Answer That Satisfied','22 The Answer That Was True']
                   ]
        
        self._characters = {
                'Hari Seldon': ['Hari Seldon', 'Hari', 'Seldon'],
                'Gaal Dornick': ['Gaal Dornick', 'Gaal', 'Dornick'],
                'Jerril': ['Jerril'],
                'Linge Chen': ['Linge Chen', 'Linge', 'Chen'],
                'Lors Avakim': ['Lors Avakim', 'Lors', 'Avakim'],
                'Salvor Hardin': ['Salvor Hardin', 'Salvor', 'Hardin'],
                'Bor Alurin': ['Bor Alurin', 'Bor', 'Alurin'],
                'Jord Fara': ['Jord Fara', 'Jord', 'Fara'],
                'Lewis Pirenne': ['Lewis Pirenne', 'Lewis', 'Pirenne'],
                'Lundin Crast': ['Lundin Crast', 'Lundin', 'Crast'],
                'Lord Dorwin': ['Lord Dorwin', 'Dorwin'],
                'Tomaz Sutt': ['Tomaz Sutt', 'Tomaz', 'Sutt'],
                'Yate Fulham': ['Yate Fulham', 'Yate', 'Fulham'],
                'Yohan Lee': ['Yohan Lee', 'Yohan', 'Lee'],
                'Dokor Walto': ['Dokor Walto', 'Dokor', 'Walto'],
                'Jaim Orsy': ['Jaim Orsy', 'Jaim', 'Orsy'],
                'King Lepold I': ['King Lepold I', 'King', 'Lepold', 'Lepold I'],
                'Lem Tarki': ['Lem Tarki', 'Lem', 'Tarki'],
                'Levi Norast': ['Levi Norast', 'Levi', 'Norast'],
                'Lewis Bort': ['Lewis Bort', 'Lewis', 'Bort'],
                'Prince Lefkin': ['Prince Lefkin', 'Lefkin'],
                'Prince Regent Wienis': ['Prince Regent Wienis', 'Wienis'],
                'Poly Verisof': ['Poly Verisof', 'Poly', 'Verisof'],
                'Sef Sermak': ['Sef Sermak', 'Sef', 'Sermak'],
                'Theo Aporat': ['Theo Aporat', 'Theo', 'Aporat'],
                'Eskel Gorov': ['Eskel Gorov', 'Eskel', 'Gorov'],
                'Limmar Ponyets': ['Limmar Ponyets', 'Limmar', 'Ponyets'],
                'Les Gorm': ['Les Gorm', 'Les', 'Gorm'],
                'Hober Mallow': ['Hober Mallow', 'Hober', 'Mallow'],
                'Publis Manlio': ['Publis Manlio', 'Publis', 'Manlio'],
                'Jorane Sutt': ['Jorane Sutt', 'Jorane', 'Sutt'],
                'Jaim Twer': ['Jaim Twer', 'Jaim', 'Twer'],
                } 
        
        if os.path.isfile('data/processed_asimov.pkl'):
            self._trilogy = Helper().load_data('data/processed_asimov.pkl')
        
        if os.path.isfile('data/tokenized_asmiov.pkl'):
            self._tokens = Helper().load_data('data/tokenized_asmiov.pkl')
          
        if os.path.isfile('data/entities.pkl'):
            self._entities = Helper().load_data('data/entities.pkl')
        
        if os.path.isfile('data/tokenized_asimov_clean.pkl'):
            self._clean_tokens = Helper().load_data('data/tokenized_asimov_clean.pkl')

    def characters(self):
        return self._characters

    def path(self):
        return self._path
    
    def chapter_headers_preprocess(self):
        return self._chapter_headers_preprocess

    def chapter_headers(self):
        return self._chapter_headers
    
    def trilogy(self):
        return self._trilogy
    
    def tokens(self):
        return self._tokens
    
    def entities(self):
        return self._entities
    
    def clean_tokens(self):
        return self._clean_tokens
