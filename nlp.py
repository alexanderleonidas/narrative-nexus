from utils.preprocess import Preprocess
from utils.stanford import Stanford
from utils.helper import Helper

# Imports
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from datasets import Dataset
import networkx as nx

# Path to data
pdf_path = "data/the_foundation.pdf"

# List for storing chapter headers
chapter_headers = [
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


preprocess = Preprocess(pdf_path, chapter_headers)
stanford = Stanford()
helper = Helper()

print('Preprocessing...')
books, raw_text = preprocess.preprocess()
print('Using Stanza...')
stanford.extract_information(raw_text)
entities, relationships, sentiments = stanford.extract_information(raw_text)
print('Saving results...')
helper.save_data(entities, 'data/NER_results.pkl')
helper.save_data(relationships, 'data/relationships_results.pkl')
helper.save_data(sentiments, 'data/sentiment_results.pkl')