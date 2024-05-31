class Asimov:
    def __init__(self) -> None:
        self._path = "data/the_foundation.pdf"
        self._chapter_headers = [
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
        
        self._chapter_headers_preprocess = [
                ['PART I\nTHE PSYCHOHISTORIANS', 'PART II\nTHE ENCYCLOPEDISTS','PART III\nTHE MAYORS', 'PART IV\nTHE TRADERS',
                 'PART V\nTHE MERCHANT PRINCES'],
                ['PROLOGUE', '1. SEARCH FOR MAGICIANS', '2. THE MAGICIANS','3. THE DEAD HAND', '4. THE EMPEROR', '5. THE WAR BEGINS',
                 '6. THE FAVORITE', '7. BRIBERY', '8. TO TRANTOR', '9. ON TRANTOR', '10. THE WAR ENDS', '11. BRIDE AND GROOM',
                 '12. CAPTAIN AND MAYOR', '13. LIEUTENANT AND CLOWN', '14. THE MUTANT', '15. THE PSYCHOLOGIST', '16. CONFERENCE',
                 '17. THE VISI-SONOR', '18. FALL OF THE FOUNDATION', '19. START OF THE SEARCH', '20. CONSPIRATOR', '21. INTERLUDE IN SPACE',
                 '22. DEATH ON NEOTRANTOR', '23. THE RUINS OF TRANTOR', '24. CONVERT', '25. DEATH OF A PSYCHOLOGIST', '26. END OF THE SEARCH'],
                ['Prologue', '1\nTwo Men and the Mule', '2\nTwo Men without the Mule', '3\nTwo Men and a Peasant','4\n\nTwo Men and the Elders',
                 '5\nOne Man and the Mule', '6\nOne Man, the Mule - and Another', '7\nArcadia', '8\nSeldon\'s Plan', '9\nThe Conspirators',
                 '10\nApproaching Crisis', '11\nStowaway', '12\nLord', '13\nLady', '14\n\nAnxiety', '15 Through the Grid', '16\n\nBeginning of War',
                 '17\nWar', '18\nGhost of a World', '19\nEnd of War', '20\n\n"I Know ..."', '21\nThe Answer That Satisfied','22\nThe Answer That Was True']
                   ]
        
        self.known_character = ['Hari Seldon', 'Gaal Dornick', 'Jerril', 'Linge Chen', 'Lors Avakim', 'Salvor Hardin', 'Bor Alurin', 'Jord Fara', 
                                'Lewis Pirenne', 'Lundin Crast', 'Lord Dorwin', 'Tomaz Sutt', 'Yate Fulham', 'Yohan Lee', 'Dokor Walto', 'Jaim Orsy',
                                'King Lepold I', 'Lem Tarki', 'Levi Norast', 'Lewis Bort', 'Prince Lefkin', 'Prince Regent Wienis', 'Poly Verisof',
                                'Sef Sermak', 'Theo Aporat', 'Eskel Gorov', 'Limmar Ponyets', 'Les Gorm', 'Hober Mallow', 'Publis Manlio',
                                'Jorane Sutt', 'Jaim Twer']

    def path(self):
        return self._path
    
    def chapter_headers_preprocess(self):
        return self._chapter_headers_preprocess

    def chapter_headers(self):
        return self._chapter_headers

