import re
import fitz
from num2words import num2words
from utils.asimov import Asimov

class Preprocess:
    def __init__(self, asimov: Asimov) -> None:
        self.path = asimov.path()
        self.chapter_headers = asimov.chapter_headers()
    
    def preprocess_asimov(self):
        trilogy = self.extract_books(self.extract_pages_from_pdf(self.path))
        # Split the books up into chapters and paragraphs and get the raw text
        trilogy = [self.extract_chapters(book, self.chapter_headers[i]) for i, book in enumerate(trilogy)]
        # Remove the last chapter of the first book as it is about the author
        trilogy[0].popitem()

        return trilogy
    
    def extract_books(self, pages):
        # Split up the books and clean the text
        # It is known that the cover page of each book start at page 8, 168, and 331 respectively
        books = [
            self.clean_text(self.join_text(pages[8:167])),
            self.clean_text(self.join_text(pages[167:331])),
            self.clean_text(self.join_text(pages[331:]))
        ]

        # Now remove the contents of each book
        books[0] = self.remove_substring(books[0], 'Contents Introduction Part I The Psychohistorians Part II The Encyclopedists Part III The Mayors Part IV The Traders Part V The Merchant Princes ',)
        books[1] = self.remove_substring(books[1], 'Contents PROLOGUE  PART I THE GENERAL 1. SEARCH FOR MAGICIANS 2. THE MAGICIANS 3. THE DEAD HAND 4. THE EMPEROR 5. THE WAR BEGINS 6. THE FAVORITE 7. BRIBERY 8. TO TRANTOR 9. ON TRANTOR 10. THE WAR ENDS PART II THE MULE 11. BRIDE AND GROOM 12. CAPTAIN AND MAYOR 13. LIEUTENANT AND CLOWN 14. THE MUTANT 15. THE PSYCHOLOGIST 16. CONFERENCE 17. THE VISI-SONOR 18. FALL OF THE FOUNDATION 19. START OF THE SEARCH 20. CONSPIRATOR 21. INTERLUDE IN SPACE 22. DEATH ON NEOTRANTOR 23. THE RUINS OF TRANTOR  24. CONVERT 25. DEATH OF A PSYCHOLOGIST 26. END OF THE SEARCH ')
        books[2] = self.remove_substring(books[2], 'Contents PROLOGUE PART I SEARCH BY THE MULE 1. TWO MEN AND THE MULE First Interlude 2. TWO MEN WITHOUT THE MULE Second Interlude 3. TWO MEN AND A PEASANT Third Interlude 4. TWO MEN AND THE ELDERS Fourth Interlude 5. ONE MAN AND THE MULE 6. ONE MAN, THE MULE – AND ANOTHER Last Interlude PART II SEARCH BY THE FOUNDATION 7. ARCADIA 8. SELDON\'S PLAN 9. THE CONSPIRATORS 10. APPROACHING CRISIS 11. STOWAWAY 12. LORD  13. LADY 14. ANXIETY 15. THROUGH THE GRID 16. BEGINNING OF WAR 17. WAR 18. GHOST OF A WORLD 19. END OF WAR 20. "I KNOW ..." 21. THE ANSWER THAT SATISFIED 22. THE ANSWER THAT WAS TRUE ')

        return books

    
    def extract_chapters(self, text: str, headers):
        results = {}
        for i in range(len(headers) - 1):
            sub1, sub2 = headers[i], headers[i + 1] # Set two substrings
            try: # Get the text in between the two substrings
                after_sub1 = text.split(sub1, 1)[1]
                result = after_sub1.split(sub2, 1)[0]
                results[sub1] = result.strip()

            except IndexError:
                results[sub1] = None
        # Get the last chapter as there is none after it
        if headers and headers[-1] in text:
            last_header_index = text.index(headers[-1]) + len(headers[-1])
            remaining_text = text[last_header_index:]
            results[headers[-1]] = remaining_text.strip()
            
        return results
    
    def clean_text(self, text: str, all=False):
        if all:
            text = self.convert_to_lowercase(text)
            text = self.remove_punctuation(text)
            text = self.convert_numbers_to_words(text) 
        text = self.remove_escape_chars(text)
        return text

    @staticmethod
    def remove_escape_chars(text: str):
        return re.sub(r'\n+', ' ', text)
    
    @staticmethod
    def convert_to_lowercase(text: str):
        return text.lower()
    
    @staticmethod
    def remove_punctuation(text: str):
        return re.sub(r'[^\w\s]', '', text)

    @staticmethod
    def join_text(text: str):
        return ' '.join(text)

    @staticmethod
    def remove_substring(original_string: str, substring_to_remove: str):
        modified_string = original_string.replace(substring_to_remove, "")
        return modified_string
    
    @staticmethod
    def convert_numbers_to_words(text: str):
        # Function to replace each match
        def replace_with_words(match):
            number = int(match.group())
            return num2words(number)
        # Replacing all occurrences of numbers in the text with their word equivalents
        cleaned_text = re.sub(r'\b\d+\b', replace_with_words, text)
        return cleaned_text

    @staticmethod
    def extract_pages_from_pdf(pdf_path: str):
        doc = fitz.open(pdf_path)
        pages = [page.get_text() for page in doc]
        doc.close()
        return [page for page in pages]    