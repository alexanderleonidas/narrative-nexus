from utils.helper import Helper
from utils.preprocess import Preprocess

books = Helper().load_data('data/entities.pkl')

print(books[0].keys())