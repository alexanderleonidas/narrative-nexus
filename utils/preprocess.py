import re
import fitz

class Preprocess:
    def __init__(self, pdf_path, chapter_headers) -> None:
        self.path = pdf_path
        self.chapter_headers = chapter_headers
    
    def preprocess(self):
        trilogy_pages = self.extract_pages_from_pdf(self.path)
        trilogy_pages = [self.remove_escape_chars(page) for page in trilogy_pages]

        # Split up the book into chapters and join the pages
        # It is known that the cover page of each book start at page 8, 168, and 331 respectively
        books = [
            self.join_text(trilogy_pages[8:167]),
            self.join_text(trilogy_pages[167:331]),
            self.join_text(trilogy_pages[331:])
        ]

        # Now remove the contents of each book for easier processing
        books[0] = self.remove_substring(books[0], 'Contents Introduction Part I The Psychohistorians Part II The Encyclopedists Part III The Mayors Part IV The Traders Part V The Merchant Princes ',)
        books[1] = self.remove_substring(books[1], 'Contents PROLOGUE  PART I THE GENERAL 1. SEARCH FOR MAGICIANS 2. THE MAGICIANS 3. THE DEAD HAND 4. THE EMPEROR 5. THE WAR BEGINS 6. THE FAVORITE 7. BRIBERY 8. TO TRANTOR 9. ON TRANTOR 10. THE WAR ENDS PART II THE MULE 11. BRIDE AND GROOM 12. CAPTAIN AND MAYOR 13. LIEUTENANT AND CLOWN 14. THE MUTANT 15. THE PSYCHOLOGIST 16. CONFERENCE 17. THE VISI-SONOR 18. FALL OF THE FOUNDATION 19. START OF THE SEARCH 20. CONSPIRATOR 21. INTERLUDE IN SPACE 22. DEATH ON NEOTRANTOR 23. THE RUINS OF TRANTOR  24. CONVERT 25. DEATH OF A PSYCHOLOGIST 26. END OF THE SEARCH ')
        books[2] = self.remove_substring(books[2], 'Contents PROLOGUE PART I SEARCH BY THE MULE 1. TWO MEN AND THE MULE First Interlude 2. TWO MEN WITHOUT THE MULE Second Interlude 3. TWO MEN AND A PEASANT Third Interlude 4. TWO MEN AND THE ELDERS Fourth Interlude 5. ONE MAN AND THE MULE 6. ONE MAN, THE MULE – AND ANOTHER Last Interlude PART II SEARCH BY THE FOUNDATION 7. ARCADIA 8. SELDON\'S PLAN 9. THE CONSPIRATORS 10. APPROACHING CRISIS 11. STOWAWAY 12. LORD  13. LADY 14. ANXIETY 15. THROUGH THE GRID 16. BEGINNING OF WAR 17. WAR 18. GHOST OF A WORLD 19. END OF WAR 20. "I KNOW ..." 21. THE ANSWER THAT SATISFIED 22. THE ANSWER THAT WAS TRUE ')

        # Split the book up into chapters
        books = [self.extract_chapters(book, self.chapter_headers[i]) for i, book in enumerate(books)]
        raw_text = self.join_text([self.join_text(chapter_text for chapter_text in book.values() if chapter_text) for book in books])

        return books, raw_text

    @staticmethod
    def remove_escape_chars(text):
        return re.sub(r'\n+', ' ', text)

    @staticmethod
    def join_text(text):
        return ' '.join(text)

    @staticmethod
    def remove_substring(original_string: str, substring_to_remove):
        modified_string = original_string.replace(substring_to_remove, "")
        return modified_string

    @staticmethod
    def extract_pages_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        pages = [page.get_text() for page in doc]
        doc.close()
        return pages

    @staticmethod
    def extract_chapters(text: str, headers):
        results = {}
        for i in range(len(headers) - 1):
            sub1, sub2 = headers[i], headers[i + 1]
            try:
                after_sub1 = text.split(sub1, 1)[1]
                result = after_sub1.split(sub2, 1)[0]
                results[sub1] = result.strip()

            except IndexError:
                results[sub1] = None

        if headers and headers[-1] in text:
            last_header_index = text.index(headers[-1]) + len(headers[-1])
            remaining_text = text[last_header_index:]
            results[headers[-1]] = remaining_text.strip()
            
        return results